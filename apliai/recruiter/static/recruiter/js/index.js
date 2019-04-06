$(function() {
	var $wrapper = $('#wrapper');

	// show current input values
	$('select.selectized,input.selectized', $wrapper).each(function() {
		var $container = $('<div>').addClass('value').html('Current Value: ');
		var $value = $('<span>').appendTo($container);
		var $input = $(this);
		var update = function(e) { $value.text(JSON.stringify($input.val()));console.log($input.val()); }

		$(this).on('change', update);
		update();

		$container.insertAfter($input);
	});
});