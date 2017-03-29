$("#select_all").change(function() {
	$(".cbx").prop('checked', $(this).prop("checked"));
});

$('.cbx').change(function() {
	if (false == $(this).prop("checked")) {
		$("#select_all").prop('checked', false);
	}
	if ($('.cbx:checked').length == $('.cbx').length) {
		$("#select_all").prop('checked', true);
	}
});