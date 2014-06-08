function createSlugs(){
	// FIXME could be neater JS...
	$("#id_slug").each(function() {
		$(this).slugify("#id_" + $(this).data("slug-from"));
	})
}
