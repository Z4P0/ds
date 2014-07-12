'use strict';






ds.users = (function() {
  var $loginForm;

  var init = function() {
    if (ds.localStorage.loggedIn === true) {
      console.log('logged in');
      ds.users.loggedIn();
    } else if (ds.localStorage.loggedIn === false) {
    	console.log('logged out');
    }

		if ($('#login-form-wrapper').length) {
	    $loginForm = $('#login-form');
	    document.getElementById('login-form').addEventListener('keypress', 
	    	function (e) {if (e.keyCode === 13) dummyLogin(); }, false);    
	    $loginForm.find('input[type="submit"]').click(function(e) {
	    	e.preventDefault();
	    	dummyLogin();
	    });
	  }
  };


  var dummyLogin = function(e) {
  	// get login info from form
  	// set it to the local object
  	ds.localStorage.loggedIn = true;
  	ds.localStorage.username = $loginForm.find('input[type="text"]').val();
  	ds.localStorage.bookmarks = [
  		'Tottenham Hotspur and US U17 Team Highlight 2013 IMG Invitational Tournament',
  		'Leones Negros is the Liga Ascenso MX Apertura 2013 Champion!',
  		'Mexico U-17 Coasts Past Argentina 3-0 En Route to the Final',
  		'Raúl “Potro” Gutiérrez sent out the same starting line-up from the victory over Italy to face Brazil.',
  		'Mexico’s Shaky Start in the U-17 World Cup'
  	]
  	ds.users.save();
  	// console.log($loginForm.find('input[type="password"]').val());
  }

  var loggedIn = function(e) {
  	var $signIn = $('#sign-in');
  	// $signIn.find('a').html('Profile');
  	$signIn.find('a').attr('href','04-profile.html').html('Profile');
  	$('#logout').click(function(e) {
  		ds.users.del();
  	})

  	// populate bookmarks
  	console.log(ds.localStorage.bookmarks);
  	// $(ds.localStorage.bookmarks).each(function(i, title) {
  	// 	console.log(title);
  	// });
  	// $('#bookmarked-articles-list')

  	// set user name
  	$('#username').html(ds.localStorage.username)
  }

  var save = function(e) {
		localStorage.setItem('ds', JSON.stringify(ds.localStorage));
  }

  var del = function(e) {
  	localStorage.removeItem('ds');
  }

  return {
    init : init,
    loggedIn: loggedIn,
    save: save,
    del: del
  };
})();