const ui = $("#item_search");
const item_list = $("#item_results");
var is_local = '';

if ($(location).attr('href').includes('local_site')) {
	is_local = '/local_site';
}

const endpoint = is_local.concat('/item_results');
const d_lay = 700;
let scheduled = false;
let sub = true;

let tag_search = function(endpoint, tag_in) {
	$.getJSON(endpoint, tag_in)
		.done(response => {
			item_list.html(response['item_results_view'])
			item_list.focus()
		})
};

ui.on('keyup', function () {
	const item_in = {
		q: $(this).val()
	}

	if (scheduled) {
		clearTimeout(scheduled)
	}

	if (item_in.q.length > 0){
		scheduled = setTimeout(tag_search, d_lay, endpoint, item_in)
	}
});

ui.on('change', function() {
	let options = $(".results");
	for (let i = 0; i < options.length; i++) {
		if (options[i].value == $(this).val()) {
			submit();
			break;
		}
	}
});
