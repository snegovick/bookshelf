function ModWidgets() {};

ModWidgets.prototype = {
  login_button_template: "./auth_reg.dtpl",
  login_button_div_id: "#auth-contents",

  content_div_id: "#content",
  active_zone_div_id: "#active-zone",
  buttons_div_id: "#buttons",
  
  list_get_rq: "/api/getlist",
  list_template: "./list.dtpl",
  list_buttons_template: "./list_buttons.dtpl",
  list_add_book_button_a: "#add-book-a",
  list_add_book_button_s: "#add-book-s",
  list_edit_book_template: "./edit_book.dtpl",
  list_sort_storage_a: "a#sort-storage",
  list_sort_name_a: "a#sort-name",
  list_sort_author_a: "a#sort-author",
  list_sort_storage_s: "a#sort-storage > span",
  list_sort_name_s: "a#sort-name > span",
  list_sort_author_s: "a#sort-author > span",

  book_get_rq: "/api/getbook/"
};

var mod_widgets = new ModWidgets();
