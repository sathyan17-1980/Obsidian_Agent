/**
 * Customer Journey Analysis SDK
 *
 * Lightweight JavaScript SDK for tracking customer interactions on websites.
 *
 * Features:
 * - Automatic page view tracking
 * - Click event tracking
 * - Form interaction tracking
 * - Scroll depth tracking
 * - E-commerce events (add to cart, purchase)
 * - Offline queue with retry logic
 * - Privacy-compliant (GDPR, CCPA)
 * - < 15KB gzipped
 *
 * @version 1.0.0
 * @license MIT
 */

// =============================================================================
// Types & Interfaces
// =============================================================================

interface SDKConfig {
    /** API endpoint URL */
    apiUrl: string;

    /** API key for authentication */
    apiKey?: string;

    /** Enable automatic page view tracking */
    autoPageViews?: boolean;

    /** Enable automatic click tracking */
    autoClicks?: boolean;

    /** Enable automatic scroll tracking */
    autoScroll?: boolean;

    /** Enable automatic form tracking */
    autoForms?: boolean;

    /** Batch size for event sending (1-100) */
    batchSize?: number;

    /** Flush interval in milliseconds */
    flushInterval?: number;

    /** Enable debug logging */
    debug?: boolean;

    /** Respect Do Not Track header */
    respectDNT?: boolean;

    /** Cookie domain (for cross-domain tracking) */
    cookieDomain?: string;

    /** Cookie expiration days */
    cookieExpiration?: number;

    /** Custom device ID (optional) */
    deviceId?: string;

    /** Custom user ID (optional, set after login) */
    userId?: string;
}

interface TrackingEvent {
    event_id: string;
    timestamp: string;  // ISO 8601
    session_id: string;
    device_id: string;
    user_id?: string;
    event_type: string;
    page_url: string;
    page_title: string;
    referrer?: string;
    element_selector?: string;
    element_text?: string;
    coordinates?: [number, number];
    scroll_depth?: number;
    user_agent: string;
    screen_resolution: [number, number];
    viewport_size: [number, number];
    device_type: 'desktop' | 'mobile' | 'tablet';
    custom_properties?: Record<string, any>;
}

interface QueuedEvent {
    event: TrackingEvent;
    retries: number;
    timestamp: number;
}

// =============================================================================
// Customer Journey SDK Class
// =============================================================================

class CustomerJourneySDK {
    private config: Required<SDKConfig>;
    private sessionId: string;
    private deviceId: string;
    private userId?: string;
    private eventQueue: QueuedEvent[] = [];
    private flushTimer?: number;
    private pageViewTracked: boolean = false;
    private scrollDepth: number = 0;
    private sessionStartTime: number;

    // Constants
    private readonly MAX_QUEUE_SIZE = 100;
    private readonly MAX_RETRIES = 3;
    private readonly RETRY_DELAY = 2000;  // 2 seconds
    private readonly STORAGE_KEY_PREFIX = 'cj_';

    /**
     * Initialize the Customer Journey SDK
     *
     * @param config - SDK configuration
     */
    constructor(config: SDKConfig) {
        // Validate required config
        if (!config.apiUrl) {
            throw new Error('CustomerJourneySDK: apiUrl is required');
        }

        // Set defaults
        this.config = {
            apiUrl: config.apiUrl,
            apiKey: config.apiKey,
            autoPageViews: config.autoPageViews ?? true,
            autoClicks: config.autoClicks ?? true,
            autoScroll: config.autoScroll ?? true,
            autoForms: config.autoForms ?? true,
            batchSize: config.batchSize ?? 10,
            flushInterval: config.flushInterval ?? 5000,
            debug: config.debug ?? false,
            respectDNT: config.respectDNT ?? true,
            cookieDomain: config.cookieDomain ?? window.location.hostname,
            cookieExpiration: config.cookieExpiration ?? 365,
            deviceId: config.deviceId ?? '',
            userId: config.userId ?? '',
        };

        // Check Do Not Track
        if (this.config.respectDNT && this.isDNTEnabled()) {
            this.log('Do Not Track is enabled, SDK will not track events');
            return;
        }

        // Initialize IDs
        this.deviceId = this.config.deviceId || this.getOrCreateDeviceId();
        this.sessionId = this.getOrCreateSessionId();
        this.userId = this.config.userId;
        this.sessionStartTime = Date.now();

        // Load queued events from storage
        this.loadQueueFromStorage();

        // Set up automatic tracking
        this.setupAutoTracking();

        // Set up periodic flush
        this.startPeriodicFlush();

        // Set up beforeunload handler to flush on page exit
        window.addEventListener('beforeunload', () => this.flush(true));

        this.log('SDK initialized', {
            sessionId: this.sessionId,
            deviceId: this.deviceId,
            userId: this.userId,
        });
    }

    // =========================================================================
    // Public API Methods
    // =========================================================================

    /**
     * Track a custom event
     *
     * @param eventType - Type of event (e.g., 'button_click', 'video_play')
     * @param properties - Additional event properties
     */
    public track(eventType: string, properties?: Record<string, any>): void {
        const event = this.createBaseEvent(eventType);

        if (properties) {
            event.custom_properties = properties;
        }

        this.enqueueEvent(event);
        this.log('Event tracked', { eventType, properties });
    }

    /**
     * Track a page view
     *
     * @param pagePath - Optional custom page path
     */
    public trackPageView(pagePath?: string): void {
        const event = this.createBaseEvent('page_view');

        if (pagePath) {
            event.page_url = window.location.origin + pagePath;
        }

        this.enqueueEvent(event);
        this.pageViewTracked = true;
        this.log('Page view tracked', { url: event.page_url });
    }

    /**
     * Track e-commerce add to cart event
     *
     * @param product - Product details
     */
    public trackAddToCart(product: {
        id: string;
        name: string;
        price: number;
        quantity?: number;
        category?: string;
    }): void {
        const event = this.createBaseEvent('add_to_cart');
        event.custom_properties = {
            product_id: product.id,
            product_name: product.name,
            product_price: product.price,
            quantity: product.quantity || 1,
            product_category: product.category,
        };

        this.enqueueEvent(event);
        this.log('Add to cart tracked', product);
    }

    /**
     * Track purchase/conversion event
     *
     * @param order - Order details
     */
    public trackPurchase(order: {
        orderId: string;
        total: number;
        items: Array<{
            id: string;
            name: string;
            price: number;
            quantity: number;
        }>;
    }): void {
        const event = this.createBaseEvent('purchase');
        event.custom_properties = {
            order_id: order.orderId,
            order_total: order.total,
            items: order.items,
        };

        this.enqueueEvent(event);
        this.log('Purchase tracked', order);
    }

    /**
     * Identify a user (call after login)
     *
     * @param userId - Unique user identifier
     * @param attributes - Additional user attributes
     */
    public identify(userId: string, attributes?: Record<string, any>): void {
        this.userId = userId;
        this.config.userId = userId;

        // Track identify event
        const event = this.createBaseEvent('login');
        event.user_id = userId;

        if (attributes) {
            event.custom_properties = attributes;
        }

        this.enqueueEvent(event);
        this.log('User identified', { userId, attributes });
    }

    /**
     * Reset user identification (call after logout)
     */
    public reset(): void {
        this.userId = undefined;
        this.config.userId = '';

        // Track logout event
        const event = this.createBaseEvent('logout');
        this.enqueueEvent(event);

        this.log('User reset (logged out)');
    }

    /**
     * Manually flush queued events
     *
     * @param synchronous - Use sendBeacon for synchronous send (on page unload)
     */
    public flush(synchronous: boolean = false): void {
        if (this.eventQueue.length === 0) {
            return;
        }

        this.log(`Flushing ${this.eventQueue.length} events`, { synchronous });
        this.sendEvents(synchronous);
    }

    // =========================================================================
    // Private Helper Methods
    // =========================================================================

    /**
     * Set up automatic event tracking based on config
     */
    private setupAutoTracking(): void {
        // Auto page view tracking
        if (this.config.autoPageViews && !this.pageViewTracked) {
            this.trackPageView();
        }

        // Auto click tracking
        if (this.config.autoClicks) {
            document.addEventListener('click', (e) => this.handleClick(e), true);
        }

        // Auto scroll tracking
        if (this.config.autoScroll) {
            let scrollTimer: number;
            window.addEventListener('scroll', () => {
                clearTimeout(scrollTimer);
                scrollTimer = window.setTimeout(() => this.handleScroll(), 500);
            });
        }

        // Auto form tracking
        if (this.config.autoForms) {
            document.addEventListener('submit', (e) => this.handleFormSubmit(e), true);
            document.addEventListener('focus', (e) => this.handleFormInput(e), true);
        }
    }

    /**
     * Handle click events
     */
    private handleClick(e: MouseEvent): void {
        const target = e.target as HTMLElement;

        // Skip if target is null or not an element
        if (!target || !target.tagName) {
            return;
        }

        const event = this.createBaseEvent('click');
        event.element_selector = this.getElementSelector(target);
        event.element_text = target.textContent?.trim().slice(0, 200);
        event.coordinates = [e.clientX, e.clientY];

        this.enqueueEvent(event);
    }

    /**
     * Handle scroll events
     */
    private handleScroll(): void {
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const currentScrollDepth = Math.round((scrollTop / scrollHeight) * 100);

        // Only track if scroll depth increased significantly (by 25%)
        if (currentScrollDepth >= this.scrollDepth + 25) {
            this.scrollDepth = currentScrollDepth;

            const event = this.createBaseEvent('scroll');
            event.scroll_depth = this.scrollDepth;

            this.enqueueEvent(event);
        }
    }

    /**
     * Handle form submit events
     */
    private handleFormSubmit(e: Event): void {
        const form = e.target as HTMLFormElement;

        const event = this.createBaseEvent('form_submit');
        event.element_selector = this.getElementSelector(form);
        event.custom_properties = {
            form_id: form.id || null,
            form_name: form.name || null,
        };

        this.enqueueEvent(event);
    }

    /**
     * Handle form input events
     */
    private handleFormInput(e: FocusEvent): void {
        const target = e.target as HTMLInputElement;

        // Only track form fields
        if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) {
            return;
        }

        const event = this.createBaseEvent('form_input');
        event.element_selector = this.getElementSelector(target);
        event.custom_properties = {
            field_name: target.name || null,
            field_type: target.type || null,
        };

        this.enqueueEvent(event);
    }

    /**
     * Create base event object with common properties
     */
    private createBaseEvent(eventType: string): TrackingEvent {
        return {
            event_id: this.generateEventId(),
            timestamp: new Date().toISOString(),
            session_id: this.sessionId,
            device_id: this.deviceId,
            user_id: this.userId,
            event_type: eventType,
            page_url: window.location.href,
            page_title: document.title,
            referrer: document.referrer || undefined,
            user_agent: navigator.userAgent,
            screen_resolution: [screen.width, screen.height],
            viewport_size: [window.innerWidth, window.innerHeight],
            device_type: this.getDeviceType(),
        };
    }

    /**
     * Add event to queue and trigger flush if batch size reached
     */
    private enqueueEvent(event: TrackingEvent): void {
        // Add to queue
        this.eventQueue.push({
            event,
            retries: 0,
            timestamp: Date.now(),
        });

        // Save to storage for offline resilience
        this.saveQueueToStorage();

        // Flush if batch size reached
        if (this.eventQueue.length >= this.config.batchSize) {
            this.flush();
        }

        // Enforce max queue size (drop oldest if exceeded)
        if (this.eventQueue.length > this.MAX_QUEUE_SIZE) {
            this.eventQueue.shift();
            this.log('Queue size exceeded, dropping oldest event');
        }
    }

    /**
     * Send queued events to API
     */
    private async sendEvents(synchronous: boolean = false): Promise<void> {
        if (this.eventQueue.length === 0) {
            return;
        }

        const events = this.eventQueue.splice(0, this.config.batchSize);
        const payload = events.map(q => q.event);

        const url = `${this.config.apiUrl}/api/v1/events/batch`;
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        };

        if (this.config.apiKey) {
            headers['Authorization'] = `Bearer ${this.config.apiKey}`;
        }

        try {
            if (synchronous && navigator.sendBeacon) {
                // Use sendBeacon for synchronous send (on page unload)
                const blob = new Blob([JSON.stringify({ events: payload })], {
                    type: 'application/json',
                });
                navigator.sendBeacon(url, blob);
                this.log(`Sent ${payload.length} events via sendBeacon`);
            } else {
                // Use fetch for async send
                const response = await fetch(url, {
                    method: 'POST',
                    headers,
                    body: JSON.stringify({ events: payload }),
                    keepalive: true,  // Keep connection alive on page unload
                });

                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }

                this.log(`Sent ${payload.length} events successfully`);
            }

            // Clear from storage on success
            this.saveQueueToStorage();

        } catch (error) {
            this.log('Failed to send events, will retry', error);

            // Re-add to queue for retry
            events.forEach(qe => {
                if (qe.retries < this.MAX_RETRIES) {
                    qe.retries++;
                    this.eventQueue.push(qe);
                } else {
                    this.log('Max retries exceeded, dropping event', qe.event);
                }
            });

            // Schedule retry
            setTimeout(() => this.sendEvents(), this.RETRY_DELAY);
        }
    }

    /**
     * Start periodic event flushing
     */
    private startPeriodicFlush(): void {
        this.flushTimer = window.setInterval(() => {
            this.flush();
        }, this.config.flushInterval);
    }

    /**
     * Get or create device ID (persistent across sessions)
     */
    private getOrCreateDeviceId(): string {
        const storageKey = this.STORAGE_KEY_PREFIX + 'device_id';
        let deviceId = this.getFromStorage(storageKey);

        if (!deviceId) {
            deviceId = this.generateDeviceId();
            this.saveToStorage(storageKey, deviceId, this.config.cookieExpiration);
        }

        return deviceId;
    }

    /**
     * Get or create session ID (expires after 30 minutes of inactivity)
     */
    private getOrCreateSessionId(): string {
        const storageKey = this.STORAGE_KEY_PREFIX + 'session_id';
        const sessionTimeout = 30 * 60 * 1000;  // 30 minutes

        let sessionData = this.getFromStorage(storageKey);
        let sessionId: string;
        let lastActivity: number;

        if (sessionData) {
            try {
                const parsed = JSON.parse(sessionData);
                sessionId = parsed.id;
                lastActivity = parsed.timestamp;

                // Check if session expired
                if (Date.now() - lastActivity > sessionTimeout) {
                    // Session expired, create new one
                    sessionId = this.generateSessionId();
                    this.log('Session expired, created new session');
                }
            } catch {
                sessionId = this.generateSessionId();
            }
        } else {
            sessionId = this.generateSessionId();
        }

        // Save session with current timestamp
        this.saveToStorage(storageKey, JSON.stringify({
            id: sessionId,
            timestamp: Date.now(),
        }), 1);  // 1 day cookie

        return sessionId;
    }

    /**
     * Generate unique device ID
     */
    private generateDeviceId(): string {
        // Use fingerprinting for device ID
        const components = [
            navigator.userAgent,
            screen.width + 'x' + screen.height,
            screen.colorDepth,
            new Date().getTimezoneOffset(),
            navigator.language,
            navigator.platform,
        ];

        // Simple hash function
        const hash = components.join('|');
        return 'dev_' + this.simpleHash(hash);
    }

    /**
     * Generate unique session ID
     */
    private generateSessionId(): string {
        return 'sess_' + this.generateUUID();
    }

    /**
     * Generate unique event ID
     */
    private generateEventId(): string {
        return 'evt_' + this.generateUUID();
    }

    /**
     * Generate UUID v4
     */
    private generateUUID(): string {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Simple hash function for device fingerprinting
     */
    private simpleHash(str: string): string {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;  // Convert to 32-bit integer
        }
        return Math.abs(hash).toString(36);
    }

    /**
     * Get element CSS selector
     */
    private getElementSelector(element: HTMLElement): string {
        // Try ID first
        if (element.id) {
            return `#${element.id}`;
        }

        // Try unique class
        if (element.className) {
            const classes = element.className.split(' ').filter(c => c).join('.');
            if (classes) {
                return `${element.tagName.toLowerCase()}.${classes}`;
            }
        }

        // Fall back to tag name with nth-child
        const parent = element.parentElement;
        if (parent) {
            const siblings = Array.from(parent.children);
            const index = siblings.indexOf(element) + 1;
            return `${element.tagName.toLowerCase()}:nth-child(${index})`;
        }

        return element.tagName.toLowerCase();
    }

    /**
     * Detect device type
     */
    private getDeviceType(): 'desktop' | 'mobile' | 'tablet' {
        const ua = navigator.userAgent;

        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return 'tablet';
        }

        if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
            return 'mobile';
        }

        return 'desktop';
    }

    /**
     * Check if Do Not Track is enabled
     */
    private isDNTEnabled(): boolean {
        return navigator.doNotTrack === '1' ||
               (window as any).doNotTrack === '1' ||
               (navigator as any).msDoNotTrack === '1';
    }

    /**
     * Save data to localStorage with fallback to cookie
     */
    private saveToStorage(key: string, value: string, days: number): void {
        try {
            // Try localStorage first
            localStorage.setItem(key, value);
        } catch {
            // Fallback to cookie
            const expires = new Date();
            expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
            document.cookie = `${key}=${value};expires=${expires.toUTCString()};domain=${this.config.cookieDomain};path=/;SameSite=Lax`;
        }
    }

    /**
     * Get data from localStorage with fallback to cookie
     */
    private getFromStorage(key: string): string | null {
        try {
            // Try localStorage first
            return localStorage.getItem(key);
        } catch {
            // Fallback to cookie
            const match = document.cookie.match(new RegExp('(^| )' + key + '=([^;]+)'));
            return match ? match[2] : null;
        }
    }

    /**
     * Save event queue to storage (for offline resilience)
     */
    private saveQueueToStorage(): void {
        try {
            const key = this.STORAGE_KEY_PREFIX + 'queue';
            const data = JSON.stringify(this.eventQueue.slice(0, 50));  // Limit to 50 events
            localStorage.setItem(key, data);
        } catch (error) {
            this.log('Failed to save queue to storage', error);
        }
    }

    /**
     * Load event queue from storage
     */
    private loadQueueFromStorage(): void {
        try {
            const key = this.STORAGE_KEY_PREFIX + 'queue';
            const data = localStorage.getItem(key);

            if (data) {
                this.eventQueue = JSON.parse(data);
                this.log(`Loaded ${this.eventQueue.length} queued events from storage`);
            }
        } catch (error) {
            this.log('Failed to load queue from storage', error);
        }
    }

    /**
     * Debug logging (only if debug enabled)
     */
    private log(message: string, data?: any): void {
        if (this.config.debug) {
            console.log(`[CustomerJourney] ${message}`, data || '');
        }
    }
}

// =============================================================================
// Export & Global Initialization
// =============================================================================

// Export for module systems
export default CustomerJourneySDK;

// Auto-initialize from script tag data attributes
if (typeof window !== 'undefined') {
    const script = document.currentScript as HTMLScriptElement;

    if (script && script.dataset.apiUrl) {
        const config: SDKConfig = {
            apiUrl: script.dataset.apiUrl,
            apiKey: script.dataset.apiKey,
            autoPageViews: script.dataset.autoPageViews !== 'false',
            autoClicks: script.dataset.autoClicks !== 'false',
            autoScroll: script.dataset.autoScroll !== 'false',
            autoForms: script.dataset.autoForms !== 'false',
            debug: script.dataset.debug === 'true',
        };

        // Auto-initialize and expose globally
        (window as any).customerJourney = new CustomerJourneySDK(config);
    }
}
