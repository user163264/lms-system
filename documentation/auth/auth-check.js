// Authentication check for documentation pages
(function() {
    // Skip auth check for login page itself
    if (window.location.pathname.endsWith('/login.html')) {
        return;
    }
    
    // Check if user is authenticated
    const isAuthenticated = sessionStorage.getItem('lmsDocsAuth') === 'true';
    
    if (!isAuthenticated) {
        // Redirect to login page
        window.location.href = '/docs/auth/login.html';
    }
})(); 