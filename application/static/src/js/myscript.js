$(document).ready(function() {

	// When user click on Buy This button
	$("[name='buy_this']").on('click', function() {

		// Grab the immediate parent of the button
		$td = $(this).parent();

		// Grab the immediate parent of $td
		$tr = $td.parent();

		// Grab the symbol of that row
		$symbol = $tr.children('.symbol_row').children('.symbol').text();

		// Send GET request to the following route
		window.location.assign('/buy?symbol='+$symbol);

	});

	// When user clicks Sell This button
	$("[name='sell_this']").on('click', function() {

		// Grab the immediate parent of the button
		$td = $(this).parent();

		// Grab the immediate parent of $td
		$tr = $td.parent();

		// Grab the symbol of that row
		$symbol = $tr.children('.symbol_row').children('.symbol').text();

		// Send GET request to the following route
		window.location.assign('/sell?symbol='+$symbol);

	});

	// Insert value in password field - login form
	$('#login-pwd').val("123");

});