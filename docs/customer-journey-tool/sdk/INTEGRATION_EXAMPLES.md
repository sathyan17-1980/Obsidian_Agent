# Customer Journey SDK - Integration Examples

## Overview

This document provides comprehensive integration examples for the Customer Journey SDK across different platforms and use cases.

---

## Installation

### NPM/Yarn (Recommended for Modern Apps)

```bash
npm install @your-org/customer-journey-sdk
# or
yarn add @your-org/customer-journey-sdk
```

### CDN (Quick Setup)

```html
<script src="https://cdn.yourdomain.com/sdk/customer-journey.min.js"
        data-api-url="https://api.yourdomain.com"
        data-api-key="your-api-key-here"
        data-auto-page-views="true"
        data-auto-clicks="true"
        data-auto-scroll="true"
        data-auto-forms="true"></script>
```

---

## Basic Integration Examples

### 1. Auto-Initialization (Script Tag)

**Simplest setup - Just add the script tag:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Welcome</h1>

    <!-- Add SDK at end of body -->
    <script src="https://cdn.yourdomain.com/sdk/customer-journey.min.js"
            data-api-url="https://api.yourdomain.com"
            data-api-key="pk_live_abc123"></script>
</body>
</html>
```

**That's it!** The SDK will automatically track:
- Page views
- Clicks
- Scrolls
- Form interactions

---

### 2. Manual Initialization (JavaScript)

**For more control:**

```html
<script src="https://cdn.yourdomain.com/sdk/customer-journey.min.js"></script>
<script>
  // Initialize manually
  const tracker = new CustomerJourneySDK({
    apiUrl: 'https://api.yourdomain.com',
    apiKey: 'pk_live_abc123',

    // Configure automatic tracking
    autoPageViews: true,
    autoClicks: true,
    autoScroll: true,
    autoForms: true,

    // Performance settings
    batchSize: 10,           // Send events in batches of 10
    flushInterval: 5000,     // Flush every 5 seconds

    // Privacy settings
    respectDNT: true,        // Respect Do Not Track header

    // Debug mode (disable in production)
    debug: false
  });

  // Expose globally
  window.customerJourney = tracker;
</script>
```

---

### 3. Module Import (React, Vue, Angular)

```typescript
import CustomerJourneySDK from '@your-org/customer-journey-sdk';

// Initialize once in your app
const tracker = new CustomerJourneySDK({
  apiUrl: process.env.REACT_APP_JOURNEY_API_URL,
  apiKey: process.env.REACT_APP_JOURNEY_API_KEY,
  autoPageViews: true,
  autoClicks: true,
  debug: process.env.NODE_ENV === 'development'
});

export default tracker;
```

---

## Framework-Specific Integration

### React Integration

#### App.tsx (Initialization)

```typescript
import React, { useEffect } from 'react';
import CustomerJourneySDK from '@your-org/customer-journey-sdk';

// Initialize tracker (singleton)
const tracker = new CustomerJourneySDK({
  apiUrl: process.env.REACT_APP_JOURNEY_API_URL!,
  apiKey: process.env.REACT_APP_JOURNEY_API_KEY!,
  autoPageViews: false,  // We'll track manually in React Router
  autoClicks: true,
  autoScroll: true,
});

export const journeyTracker = tracker;

function App() {
  useEffect(() => {
    // Track initial page view
    journeyTracker.trackPageView();
  }, []);

  return (
    <div className="App">
      {/* Your app content */}
    </div>
  );
}

export default App;
```

#### Track Page Views with React Router

```typescript
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { journeyTracker } from './App';

function usePageTracking() {
  const location = useLocation();

  useEffect(() => {
    // Track page view on route change
    journeyTracker.trackPageView(location.pathname);
  }, [location]);
}

// In your main component
function AppRouter() {
  usePageTracking();

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/products" element={<Products />} />
      {/* ... */}
    </Routes>
  );
}
```

#### Custom Event Tracking (Button Click)

```typescript
import { journeyTracker } from './App';

function ProductPage() {
  const handleAddToCart = (product) => {
    // Track add to cart event
    journeyTracker.trackAddToCart({
      id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
      category: product.category
    });

    // ... rest of your add to cart logic
  };

  return (
    <button onClick={handleAddToCart}>
      Add to Cart
    </button>
  );
}
```

---

### Vue.js Integration

#### main.js (Plugin)

```javascript
import { createApp } from 'vue';
import CustomerJourneySDK from '@your-org/customer-journey-sdk';
import App from './App.vue';

// Create plugin
const journeyPlugin = {
  install(app) {
    const tracker = new CustomerJourneySDK({
      apiUrl: import.meta.env.VITE_JOURNEY_API_URL,
      apiKey: import.meta.env.VITE_JOURNEY_API_KEY,
      autoPageViews: false,
      autoClicks: true,
    });

    // Make available globally
    app.config.globalProperties.$journey = tracker;

    // Also provide via inject/provide
    app.provide('journey', tracker);
  }
};

const app = createApp(App);
app.use(journeyPlugin);
app.mount('#app');
```

#### Track Page Views with Vue Router

```javascript
import { useJourney } from './composables/useJourney';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const journey = useJourney();
    const route = useRoute();

    watch(() => route.path, (newPath) => {
      journey.trackPageView(newPath);
    });
  }
};
```

---

### Next.js Integration

#### _app.tsx

```typescript
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import CustomerJourneySDK from '@your-org/customer-journey-sdk';

// Initialize tracker (singleton)
let tracker: CustomerJourneySDK | null = null;

function getTracker() {
  if (!tracker && typeof window !== 'undefined') {
    tracker = new CustomerJourneySDK({
      apiUrl: process.env.NEXT_PUBLIC_JOURNEY_API_URL!,
      apiKey: process.env.NEXT_PUBLIC_JOURNEY_API_KEY!,
      autoPageViews: false,
      autoClicks: true,
    });
  }
  return tracker;
}

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    const tracker = getTracker();
    if (!tracker) return;

    // Track initial page view
    tracker.trackPageView(router.pathname);

    // Track route changes
    const handleRouteChange = (url: string) => {
      tracker.trackPageView(url);
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);

  return <Component {...pageProps} />;
}

export default MyApp;
```

---

## E-commerce Integration Examples

### Shopify Integration

```html
<!-- Add to theme.liquid, before </body> -->
<script src="https://cdn.yourdomain.com/sdk/customer-journey.min.js"
        data-api-url="https://api.yourdomain.com"
        data-api-key="pk_live_abc123"></script>

<script>
  // Track Shopify-specific events

  {% if template == 'product' %}
    // Product page view
    customerJourney.track('product_view', {
      product_id: {{ product.id }},
      product_name: "{{ product.title }}",
      product_price: {{ product.price | money_without_currency }},
      product_category: "{{ product.type }}"
    });
  {% endif %}

  {% if template == 'cart' %}
    // Cart page view
    customerJourney.track('cart_view', {
      cart_total: {{ cart.total_price | money_without_currency }},
      item_count: {{ cart.item_count }}
    });
  {% endif %}

  // Track add to cart (requires AJAX cart)
  document.addEventListener('cart:item-added', function(e) {
    customerJourney.trackAddToCart({
      id: e.detail.product_id,
      name: e.detail.product_title,
      price: e.detail.price,
      quantity: e.detail.quantity
    });
  });
</script>
```

---

### WooCommerce Integration

```php
<!-- Add to functions.php -->
<?php
function enqueue_customer_journey_sdk() {
    ?>
    <script src="https://cdn.yourdomain.com/sdk/customer-journey.min.js"
            data-api-url="https://api.yourdomain.com"
            data-api-key="pk_live_abc123"></script>
    <?php

    // Track WooCommerce events
    if (is_product()) {
        $product = wc_get_product(get_the_ID());
        ?>
        <script>
          window.addEventListener('load', function() {
            customerJourney.track('product_view', {
              product_id: '<?php echo $product->get_id(); ?>',
              product_name: '<?php echo $product->get_name(); ?>',
              product_price: <?php echo $product->get_price(); ?>,
              product_category: '<?php echo $product->get_category_ids()[0] ?? ''; ?>'
            });
          });
        </script>
        <?php
    }

    if (is_checkout()) {
        ?>
        <script>
          window.addEventListener('load', function() {
            customerJourney.track('checkout_started');
          });
        </script>
        <?php
    }
}
add_action('wp_footer', 'enqueue_customer_journey_sdk');

// Track purchase on order completion
function track_purchase_on_order($order_id) {
    $order = wc_get_order($order_id);
    ?>
    <script>
      customerJourney.trackPurchase({
        orderId: '<?php echo $order_id; ?>',
        total: <?php echo $order->get_total(); ?>,
        items: <?php echo json_encode(array_map(function($item) {
            return [
                'id' => $item->get_product_id(),
                'name' => $item->get_name(),
                'price' => $item->get_total(),
                'quantity' => $item->get_quantity()
            ];
        }, $order->get_items())); ?>
      });
    </script>
    <?php
}
add_action('woocommerce_thankyou', 'track_purchase_on_order');
?>
```

---

## Advanced Use Cases

### 1. User Identification (After Login)

```javascript
// After successful login
function onUserLogin(user) {
  customerJourney.identify(user.id, {
    email: user.email,  // Will be hashed on server
    name: user.name,
    plan: user.subscription_plan,
    created_at: user.created_at
  });
}

// After logout
function onUserLogout() {
  customerJourney.reset();
}
```

---

### 2. Track Video Engagement

```javascript
const video = document.querySelector('video');

video.addEventListener('play', () => {
  customerJourney.track('video_play', {
    video_id: video.dataset.id,
    video_title: video.dataset.title
  });
});

video.addEventListener('pause', () => {
  customerJourney.track('video_pause', {
    video_id: video.dataset.id,
    timestamp: video.currentTime
  });
});
```

---

### 3. Track Form Abandonment

```javascript
const form = document.querySelector('#signup-form');
let formStarted = false;

form.addEventListener('focus', (e) => {
  if (!formStarted) {
    customerJourney.track('form_started', {
      form_id: 'signup-form'
    });
    formStarted = true;
  }
}, true);

window.addEventListener('beforeunload', () => {
  if (formStarted && !formCompleted) {
    customerJourney.track('form_abandoned', {
      form_id: 'signup-form'
    });
  }
});
```

---

### 4. Track Search Queries

```javascript
const searchForm = document.querySelector('#search-form');

searchForm.addEventListener('submit', (e) => {
  const query = e.target.querySelector('input[name="q"]').value;

  customerJourney.track('search', {
    query: query,
    results_count: document.querySelectorAll('.search-result').length
  });
});
```

---

### 5. Track File Downloads

```javascript
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href]');

  if (link && link.href.match(/\.(pdf|doc|docx|xls|xlsx|zip)$/i)) {
    customerJourney.track('file_download', {
      file_name: link.href.split('/').pop(),
      file_type: link.href.split('.').pop(),
      file_url: link.href
    });
  }
});
```

---

## Privacy Compliance Examples

### 1. Cookie Consent Integration

```javascript
// Initialize SDK only after consent
function initializeTracking() {
  const tracker = new CustomerJourneySDK({
    apiUrl: 'https://api.yourdomain.com',
    apiKey: 'pk_live_abc123',
    respectDNT: true
  });

  window.customerJourney = tracker;
}

// OneTrust example
window.OptanonWrapper = function() {
  const activeGroups = window.OnetrustActiveGroups;

  // Check if analytics cookies are accepted
  if (activeGroups.includes('C0002')) {
    initializeTracking();
  }
};
```

---

### 2. GDPR Opt-Out

```javascript
// Allow users to opt out
function optOutTracking() {
  localStorage.setItem('cj_opt_out', 'true');
  location.reload();
}

// Check opt-out before initializing
if (localStorage.getItem('cj_opt_out') !== 'true') {
  // Initialize SDK
  const tracker = new CustomerJourneySDK({ /* config */ });
}
```

---

## Testing & Debugging

### Enable Debug Mode

```javascript
const tracker = new CustomerJourneySDK({
  apiUrl: 'https://api.yourdomain.com',
  apiKey: 'pk_test_abc123',  // Use test API key
  debug: true  // Enable console logging
});

// You'll see logs like:
// [CustomerJourney] SDK initialized {sessionId: "sess_...", deviceId: "dev_..."}
// [CustomerJourney] Event tracked {eventType: "page_view", properties: {...}}
// [CustomerJourney] Sent 5 events successfully
```

---

### Manual Event Inspection

```javascript
// Inspect queued events (before flush)
console.log(tracker.eventQueue);

// Manually flush events
tracker.flush();
```

---

## Performance Optimization

### 1. Lazy Load SDK

```javascript
// Load SDK only after page is interactive
if (document.readyState === 'complete') {
  loadSDK();
} else {
  window.addEventListener('load', loadSDK);
}

function loadSDK() {
  const script = document.createElement('script');
  script.src = 'https://cdn.yourdomain.com/sdk/customer-journey.min.js';
  script.async = true;
  script.dataset.apiUrl = 'https://api.yourdomain.com';
  script.dataset.apiKey = 'pk_live_abc123';
  document.body.appendChild(script);
}
```

---

### 2. Reduce Batch Size for Low-Traffic Sites

```javascript
const tracker = new CustomerJourneySDK({
  apiUrl: 'https://api.yourdomain.com',
  apiKey: 'pk_live_abc123',
  batchSize: 5,         // Smaller batches (default: 10)
  flushInterval: 10000  // Flush less frequently (default: 5000ms)
});
```

---

## Troubleshooting

### SDK Not Tracking?

1. **Check browser console** for errors
2. **Verify API URL** is correct and accessible
3. **Check Do Not Track** - SDK respects DNT by default
4. **Verify API key** is valid
5. **Check CORS** - API must allow your domain

### Events Not Appearing in Dashboard?

1. **Wait a few minutes** - events are processed asynchronously
2. **Check network tab** - verify POST requests to `/api/v1/events/batch`
3. **Enable debug mode** - see what events are being sent
4. **Check API response** - look for error messages

---

## Best Practices

### ✅ DO:
- Initialize SDK as early as possible (but after consent)
- Use batching to reduce API calls
- Respect Do Not Track
- Use test API keys in development
- Enable debug mode in development
- Hash or encrypt PII before sending

### ❌ DON'T:
- Track sensitive data (passwords, credit cards, SSNs)
- Initialize multiple SDK instances
- Track too frequently (causes performance issues)
- Hardcode production API keys in public code
- Ignore GDPR/CCPA compliance

---

## Support

**Documentation:** https://docs.yourdomain.com/sdk
**GitHub:** https://github.com/your-org/customer-journey-sdk
**Email:** support@yourdomain.com
