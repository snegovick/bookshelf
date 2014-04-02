function ModAuth() {};

ModAuth.prototype = {
  login_anchor : "#login-button",
  login_span : "#login-span",
  profile_layer_id : "#auth-form",
  login_button_id : "#login-button",
  auth_contents_id : "#auth-contents",
  login_result_id : "div#login-result",
  logout_id : "div#logout",
  login_form_id: "form#login-form",
  authed: false,
  uuid: null,

  login_click_handler: function( self ) {
    $(self.login_form_id).live('submit', function() {
      var username = $('#username').attr('value');
      var password = $('#password').attr('value');
      
      if (username && password) {
        $.ajax({type: "POST", url: "/api/login",
                contentType: "application/json; charset=utf-8",
                dataType: "json", data: "{\"username\":\""+username+"\", \"password\":\""+password+"\"}",
                error: function(xhr, status, returned_error) {
                  $('div#login-result').text("Could not sign you in");
                  $('div#login-result').addClass("error");
                },
                success: function(data) {
                  if (data.error) {
                    $('div#login-result').text("Login error "+data.error);
                    $('div#login-result').addClass("error");
                  } else { // login succeeded
                    self.show_logout_button(self);
                    console.log("login succeded");
                    self.uuid = data["data"]["uuid"];
                    //event_handler();
                  }
                }
               });
      } else {
        $('div#login-result').text("enter username and password");
        $('div#login-result').addClass("error");
      }
      $('div#login-result').fadeIn();
      return false;
    });
  },

  login_form_click_handler : function( self ) {
    self.login_click_handler(self);
    $(self.login_anchor).delegate(self.login_span, 'click', function(e) {
      //history.pushState(null, e.target.textContent, $(this).parent().attr('href'));
      console.log("login clicked");
      self.show_login_form(self);
      //event_handler();
      return false;
    });
  },

  show_login_form : function( self ){
    $(self.auth_contents_id).hide();
    $(self.profile_layer_id).show();
  },

  show_login_button : function ( self ){
    dust.render(mod_widgets.login_button_template, {}, function(err, out) {
      $(mod_widgets.login_button_div_id).html(out);
      self.login_form_click_handler(self);
      $(mod_widgets.login_button_div_id).show();
    });
  },

  hide_login_button : function ( self ) {
    $(self.login_button_div_id).hide();
  },

  hide_login_form : function( self ) {
    $(self.login_form_id).hide();
    $(self.login_result_id).hide();    
  },

  show_logout_button : function( self ) {
    self.hide_login_form(self);
    //$(self.logout_id).html("<a href=\"/\"><span id=logout-span>Log out</span></a>");
  },

  is_authed : function( self ) {
    $.ajax({type: "POST", url: "/api/getauthstatus",
            contentType: "application/json; charset=utf-8",
            dataType: "json", data: "",
            error: function(xhr, status, returned_error) {
              self.authed = false;
              mod_events.run(mod_events, "login", false);
            },
            success: function(data) {
              console.log(data);
              if (data.error!=null) {
                self.authed = false;
                mod_events.run(mod_events, "login", false);
              } else { // login succeeded
                self.uuid = data["uuid"];
                self.authed = true;
                mod_events.run(mod_events, "login", true);
              }
            }
           });

  },

  display : function( self ) {
    if (self.authed == true) {
      console.log("authed, hide everything");
      self.hide_login_form(self);
      self.hide_login_button(self);
    } else {
      console.log("show login button");
      self.show_login_button(self);
    }
  }
};

var mod_auth = new ModAuth();
