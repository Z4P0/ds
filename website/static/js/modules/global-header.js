'use strict';

// update nav --> current page
// handle search things

ds.nav = (function() {
  var $nav,
      page,
      $toggle,
      $search_li,
      $search_toggle,
      $form,
      $search_field,
      $search_results,
      $container; // this one is for when we search on miobile and darken the screen

  var init = function(_settings) {
    // nav
    $nav = $(_settings.nav);

    // page container
    $container = $('.container');


    // page (what page are we on?)
    // ----------------------------
    page = $('body').attr('data-page');
    // add class .here to <li>
    $nav.find('li').each(function(i, el) {
      if (el.getAttribute('data-page') === page) {
        el.className = 'here';
      }
    })


    // toggle main menu
    // ----------------------------
    $toggle = $(_settings.toggle);
    $toggle.click(function() {
      toggleMenu();
    });



    // search field
    // ----------------------------
    $search_li = $(_settings.search);
    $search_field = $search_li.find('#search-input');

    // set up form
    $form = $search_li.find('#search-form');
    $form.toggleClass('hidden'); // hide it


    // search form toggles
    // ----------------------------
    // set up search form toggle
    $search_toggle = $search_li.find('#search-toggle')
    $search_toggle.click(function() {toggleSearch();})
    // set up search-close btn
    $search_li.find('#search-form-close').click(function() {toggleSearch();});

    // search form results div
    // ----------------------------
    $search_results = $search_li.find('#search-results');
    $search_results.toggleClass('hidden');


    // $search_field.on('keyup', function(e) {
    //   // $search_results.toggleClass('hidden');
    //   if (e.keyCode === 27 ) toggleSearch();
    //   $.ajax({
    //     type: 'POST',
    //     url: '/search/',
    //     data: {
    //       'search_text': $search_field.val(),
    //       'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    //     },
    //     success: showResults,
    //     dataType: 'html'
    //   });
    // });

  };

  var toggleMenu = function() {
    $toggle.toggleClass('show-x');
    $nav.toggleClass('nav-show');

    // hide search form if it was left open
    if ($search_toggle.hasClass('hidden')) {
      toggleSearch();
    }
  }

  var toggleSearch = function() {
    // mobile
    if (ds.width < 768) {
      $container.toggleClass('overlay');
      $search_toggle.toggleClass('hidden');
    }
    $form.toggleClass('hidden');
    toggleResults();
  }

  var showResults = function(data, textStatus, jqXHR) {
    $search_results.html(data);
  }

  var toggleResults = function() {
    if (!$search_results.hasClass('hidden')) {
      $search_results.toggleClass('hidden');
    }
  }


  return {
    init : init
  };
})();
