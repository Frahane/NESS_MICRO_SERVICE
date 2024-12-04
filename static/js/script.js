$(document).ready(function() {
    // Initialize Telegram Web App
    if (window.Telegram.WebApp) {
        const webapp = window.Telegram.WebApp;
        webapp.ready();
        
        // Expand to full screen
        webapp.expand();

        // Enable closing confirmation
        webapp.enableClosingConfirmation();

        // Set the header color to match your app's theme
        webapp.setHeaderColor('#46a1d6');

        // You can also add a back button if needed
        webapp.BackButton.show();
        webapp.BackButton.onClick(function() {
            webapp.close();
        });

        // Log WebApp info for debugging
        console.log("Telegram WebApp initialized");
        console.log("WebApp Platform:", webapp.platform);
        console.log("WebApp Version:", webapp.version);
        console.log("WebApp InitData:", webapp.initData);
    } else {
        console.log("Telegram WebApp is not available");
    };

    // Back button functionality
    $('#back-button').on('click', function() {
        window.history.back();
    });

    // Fetch and display market data
    function fetchMarketData() {
        $.ajax({
            url: 'https://api.coingecko.com/api/v3/coins/markets',
            method: 'GET',
            data: {
                vs_currency: 'usd',
                order: 'market_cap_desc',
                per_page: 5,
                page: 1,
                sparkline: false
            },
            success: function(data) {
                $('#market-data tbody').empty();
                data.forEach(coin => {
                    $('#market-data tbody').append(`
                        <tr class='fade-in'>
                            <td>${coin.name} (${coin.symbol.toUpperCase()})</td>
                            <td>$${coin.current_price.toLocaleString()}</td>
                            <td>${coin.price_change_percentage_24h.toFixed(2)}%</td>
                        </tr>
                    `);
                });
            },
            error: function(err) {
                console.error('Error fetching market data:', err);
            }
        });
    }

    // Fetch and display signal alerts
    function fetchSignalAlerts() {
        $.ajax({
            url: 'https://api.cryptosignals.com/v1/signals', // Replace with the actual API endpoint
            method: 'GET',
            success: function(data) {
                $('#alerts').empty();
                data.slice(0, 5).forEach(signal => {
                    $('#alerts').append(`<div class='alert fade-in'>${signal.message}</div>`);
                });
            },
            error: function(err) {
                console.error('Error fetching signal alerts:', err);
            }
        });
    }

    

    // Populate bot tables
    function populateBotTable(bots, tableId) {
        const tbody = $(`#${tableId} tbody`);
        tbody.empty(); // Clear existing content
        bots.forEach(bot => {
            tbody.append(`
                <tr class='fade-in'>
                    <td><a href="https://t.me/${bot.username}?start=trade" class="telegram-bot-link">${bot.name}</a></td>
                    <td>${bot.price}</td>
                    <td>${bot.exchange}</td>
                </tr>
            `);
        });
    }

    // Define Spot and Perpetual Trading Bots
    const spotBots = [
        { name: 'Doge', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Doge_Bot' },
        { name: 'Doge', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Doge_Bot' },
        { name: 'Doge', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Doge_Bot' },
        { name: 'XRP', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_XRP_Bot' },
        { name: 'XRP', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_XRP_Bot' },
        { name: 'XRP', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_XRP_Bot' },
        { name: 'ETH', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_ETH_Bot' },
        { name: 'ETH', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_ETH_Bot' },
        { name: 'ETH', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_ETH_Bot' },
        { name: 'BTC', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_BTC_Bot' },
        { name: 'BTC', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_BTC_Bot' },
        { name: 'BTC', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_BTC_Bot' },
        { name: 'SOL', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_SOL_Binance_Bot' },
        { name: 'SOL', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_SOL_Kucoin_Bot' },
        { name: 'SOL', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_SOL_OKX_Bot' },
        { name: 'AVAX', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_AVAX_Binance_Bot' },
        { name: 'AVAX', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_AVAX_Kucoin_Bot' },
        { name: 'AVAX', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_AVAX_OKX_Bot' },
        // Add other bots here...
    ];

    const perpetualBots = [
        { name: 'Doge', price : '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Perpetual_Doge_Binance_Bot' },
        { name: 'Doge', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Perpetual_Doge_Kucoin_Bot' },
        { name: 'Doge', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Perpetual_Doge_OKX_Bot' },
        { name: 'XRP', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Perpetual_XRP_Binance_Bot' },
        { name: 'XRP', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Perpetual_XRP_Kucoin_Bot' },
        { name: 'XRP', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Perpetual_XRP_OKX_Bot' },
        { name: 'ETH', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Perpetual_ETH_Binance_Bot' },
        { name: 'ETH', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Perpetual_ETH_Kucoin_Bot' },
        { name: 'ETH', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Perpetual_ETH_OKX_Bot' },
        { name: 'BTC', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Perpetual_BTC_Binance_Bot' },
        { name: 'BTC', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Perpetual_BTC_Kucoin_Bot' },
        { name: 'BTC', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Perpetual_BTC_OKX_Bot' },
        { name: 'SOL', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Perpetual_SOL_Binance_Bot' },
        { name: 'SOL', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Perpetual_SOL_Kucoin_Bot' },
        { name: 'SOL', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Perpetual_SOL_OKX_Bot' },
        { name: 'AVAX', price: '2000 NCH', exchange: 'Binance', username: 'Stoneyard_Perpetual_AVAX_Binance_Bot' },
        { name: 'AVAX', price: '2000 NCH', exchange: 'Kucoin', username: 'Stoneyard_Perpetual_AVAX_Kucoin_Bot' },
        { name: 'AVAX', price: '2000 NCH', exchange: 'OKX', username: 'Stoneyard_Perpetual_AVAX_OKX_Bot' },
        // Add other bots here...
    ];


    // Populate the tables on page load
    populateBotTable(spotBots, "spot-bot-link");
    populateBotTable(perpetualBots, "perpetual-bot-link");

    // Fetch data on page load
    fetchMarketData();
    fetchSignalAlerts();
});