function ModList() {};

ModList.prototype = {
  post_images: [],
  book_uuid: null,
  data: null,

  render_book_template: function( self, data ) {
    if (data == null) {
      data = {"content": {"year": "", "header": "", "authors" : ""}};
    }
    dust.render(mod_widgets.list_edit_book_template, data, function(err, out) {
      console.log(out);
      $(mod_widgets.buttons_div_id).html(out);
      self.upload_image_handler(self);
      self.image_handler(self);
      self.post_book_handler(self);
    });
  },

  show_book_editor: function ( self, uuid ) {
    console.log("show_book_editor");
    console.log("uuid:"+uuid);
    if (uuid!=null && uuid!="") {
      console.log("loading book");
      self.book_uuid = uuid;
      $.getJSON(mod_widgets.book_get_rq+self.book_uuid, function(data) {
        console.log("error: "+data["error"]);
        console.log(data);
        self.post_images = data["data"]["images"];
        if (data["error"]==null) {
          self.render_book_template(self, data["data"]);
        } else {
          self.render_book_template(self, null);
        }
      });
    } else {
      self.render_book_template(self, null);      
    }
  },

  edit_book_click_handler: function( self ) {
    $('#edit-a').die('click').live('click', function(e) {
      console.log(e.target);
      var uuid = $(e.target).attr('href');
      self.show_book_editor(self, uuid);
      mod_events.edit(mod_events, uuid);
      return false;
    });
  },

  sort_author_click_handler: function( self ) {
    $(mod_widgets.list_sort_author_a).die('click').live('click', function(e) {
      if ($(mod_widgets.list_sort_author_s).attr("id") === "up") {
        self.data["entries"].sort(function(a, b) {
          if (a["content"]["authors"]>b["content"]["authors"]) {
            return 1;
          } else if ((a["content"]["authors"]===b["content"]["authors"])) {
            return 0;
          } else {
            return -1;
          }
        });
        self.display_list(self, self.data);
        $(mod_widgets.list_sort_author_s).attr("id", "down");
      } else {
        self.data["entries"].sort(function(a, b) {
          if (a["content"]["authors"]>b["content"]["authors"]) {
            return -1;
          } else if ((a["content"]["authors"]===b["content"]["authors"])) {
            return 0;
          } else {
            return 1;
          }
        });
        self.display_list(self, self.data);
        $(mod_widgets.list_sort_author_s).attr("id", "up");
      }

      return false;
    });
  },


  sort_name_click_handler: function( self ) {
    $(mod_widgets.list_sort_name_a).die('click').live('click', function(e) {
      if ($(mod_widgets.list_sort_name_s).attr("id") === "up") {
        self.data["entries"].sort(function(a, b) {
          if (a["content"]["header"]>b["content"]["header"]) {
            return 1;
          } else if ((a["content"]["header"]===b["content"]["header"])) {
            return 0;
          } else {
            return -1;
          }
        });
        self.display_list(self, self.data);
        $(mod_widgets.list_sort_name_s).attr("id", "down");
      } else {
        self.data["entries"].sort(function(a, b) {
          if (a["content"]["header"]>b["content"]["header"]) {
            return -1;
          } else if ((a["content"]["header"]===b["content"]["header"])) {
            return 0;
          } else {
            return 1;
          }
        });
        self.display_list(self, self.data);
        $(mod_widgets.list_sort_name_s).attr("id", "up");
      }

      return false;
    });
  },


  sort_storage_click_handler: function( self ) {
    $(mod_widgets.list_sort_storage_a).die('click').live('click', function(e) {
      if ($(mod_widgets.list_sort_storage_s).attr("id") === "up") {
        self.data["entries"].sort(function(a, b) {
          if (a["storeid"]>b["storeid"]) {
            return 1;
          } else if ((a["storeid"]===b["storeid"])) {
            return 0;
          } else {
            return -1;
          }
        });
        self.display_list(self, self.data);
        $(mod_widgets.list_sort_storage_s).attr("id", "down");
      } else {
        self.data["entries"].sort(function(a, b) {
          if (a["storeid"]>b["storeid"]) {
            return -1;
          } else if ((a["storeid"]===b["storeid"])) {
            return 0;
          } else {
            return 1;
          }
        });
        self.display_list(self, self.data);
        $(mod_widgets.list_sort_storage_s).attr("id", "up");
      }

      return false;
    });
  },

  post_book_handler: function( self ) {
    $('#edit-cancel').die('click').live('click', function(e) {
      mod_events.load(mod_events);
    });
    $("#book-post-form").die('submit').live('submit', function() {
      console.log("book post form");
      var header = $('#header').attr('value');
      var authors = $('#authors').attr('value');
      var year = $('#year').attr('value');
      var storeid = $('#storeid').attr('value');
      var post_data = {"uuid": self.book_uuid, "storeid": storeid, "header": header, "authors": authors, "year": year, "images":self.post_images};
      $.ajax({type: "POST", url: "/api/post_book",
              contentType: "application/json; charset=utf-8",
              dataType: "json", data: JSON.stringify(post_data),
              success: function(data) {
                console.log("error:", data.error);
                if (data.error) {
                  console.log("data error");
                } else {
                  dust.render("./list_buttons.dtpl", {}, function(err, out) {
                    $("#buttons").html(out);
                  });
                  
                  console.log("post succeded");
                  //event_handler();
                }
              }
             });
      self.book_uuid = null;
      self.post_images = [];
      mod_events.load(mod_events);
      return false;
    });
  },

  upload_image_handler : function( self ) {
    $("#upload-image").die('click').live('click', function(e) {
      $("#upload").click();
      console.log("upload clicked");
      return false;
    });
  },

  image_handler : function( self ) {
    $("#upload").change(function(f) {
      console.log("file submit");
      console.log("value: ");
      console.log($(this));
      
      
      for (var i = 0; i<$(this).context.files.length; i++) {
        var fl = $(this).context.files[i];
        var reader = new FileReader();
        console.log(fl);
        
        console.log("reading");
        reader.readAsDataURL(fl);
        
        var data = new FormData();
        data.append("file", fl);
        
        console.log(data);
        $.ajax({type: "POST", url: "/api/upload",
                contentType: false,//"multipart/form-data",
                cache: false,
                processData: false,
                data: data,
                success: function(data) {
                  console.log("error:", data.error);
                  console.log(data);
                  var f_reply = data.data.files[0];
                  console.log(f_reply);
                  
                  if (f_reply.status == true) {
                    dust.render("./image_preview.dtpl", {"width": 50, "height": 50, "imgsrc": f_reply["path"]+"thumb_"+f_reply["name"]}, function(err, out) {
                      $("#preview").append(out);
                      self.post_images.push(f_reply.name);
                    });
                  }            
                  if (data.error) {
                    console.log("data error");
                  } else {
                    console.log("upload succeded");
                  }
                }
               });
      }
    });
  },

  add_book_click_handler: function( self ) {
    $(mod_widgets.list_add_book_button_a).die('click').live('click', function(e) {
      console.log("add book handler");
      self.show_book_editor(self);
      return false;
    });
  },

  display_list: function(self, data) {
    dust.render(mod_widgets.list_template, data, function(err, out) {
      console.log("rendered:");
      console.log(out);
      $(mod_widgets.active_zone_div_id).html(out);
      dust.render(mod_widgets.list_buttons_template, {}, function(err, out) {
        $(mod_widgets.buttons_div_id).html(out);
        self.add_book_click_handler(self);
      });
      self.edit_book_click_handler(self);
      self.sort_storage_click_handler(self);
      self.sort_name_click_handler(self);
      self.sort_author_click_handler(self);
    });

  },

  request_books_list: function( self, show_buttons ) {
    $.getJSON(mod_widgets.list_get_rq, function(data) {
      console.log("error: "+data["error"]);
      console.log(data);
      if (data["error"]==null) {
        self.data = data;
        self.display_list(self, data);
      } else {
        console.log("error");
      }
    });
  },

  display : function( self ) {
    self.request_books_list(self);
  }
};

var mod_list = new ModList();
