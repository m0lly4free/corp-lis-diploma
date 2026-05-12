// Конфигурация Lighthouse CI (9.2.4.3)
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost/',
        'http://localhost/services/',
        'http://localhost/news/',
        'http://localhost/contacts/',
      ],
      settings: {
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
        // Эмуляция мобильного устройства
        formFactor: 'mobile',
        screenEmulation: {
          mobile: true,
          width: 375,
          height: 667,
          deviceScaleFactor: 2,
        },
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.8 }],
        'categories:accessibility': ['warn', { minScore: 0.9 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['warn', { maxNumericValue: 3000 }],
        'total-byte-weight': ['warn', { maxNumericValue: 2000000 }], // 2MB max
      },
    },
  },
};