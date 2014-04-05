function ModEvents() {};

ModEvents.prototype = {

  load: function( self, arg ) {
    mod_auth.is_authed(mod_auth);
    mod_list.display(mod_list);
  },
  
  login: function( self, status ) {
    mod_auth.display(mod_auth);
    if (status==true) {
      mod_state.authed = true;
      mod_state.uuid = mod_auth.uuid;
    } else {

    }
  },

  edit: function ( self, uuid ) {
    history.pushState(null, "", uuid);
  },

  handle_popstate: function( self, event ) {
    var arg = window.location.href;
    var path = arg.split('/');
    var path_root = 3;
    console.log("path root: "+path[path_root]);
    console.log("path.length: "+path.length);
    if (path[path_root]!=null) {
      mod_list.show_book_editor(mod_list, path[path_root])
    }
  },

  init: function( self ) {
    window.addEventListener('popstate', (function(s) {
      return function (event) {
        return s.handle_popstate(s, event);
      };
    })(self));
  },
  
  run: function( self, event, arg ) {
    if (ModEvents.prototype.hasOwnProperty(event)) {
      console.log("Event:");
      console.log(event);
      self[event](self, arg);
      return true;
    }
    console.log("Bad event");
    console.log(event);
    return false;
  }
};

var mod_events = new ModEvents();
