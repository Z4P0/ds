'use strict';

var ds = {}; //global var

//wait until main document is loaded
window.addEventListener('load',function(){

	// localStorage
	if (localStorage.getItem('ds') === null) {
		console.log('no localStorage');
		var test = {
			'loggedIn': false
		};
		localStorage.setItem('ds', JSON.stringify(test));
		console.log('localStorage set');
	}
	// localStorage.removeItem('ds');
	ds.localStorage = JSON.parse(localStorage.getItem('ds'));
	// var test = new ds.users.init();
	// ds.users.init();
	// console.log(test);
	// console.log(ds);




	
	// collapse certain things
	if ($('#all-topics-wrapper').length) {
		$('#all-topics-wrapper').toggle();
		$('#all-topics-toggle').on('click', function() {
			$(this).toggleClass('show-collapse');
			$('#all-topics-wrapper').toggle();
		})
	}



	// league overview
	// ===================================
	if ($('#league-overview').length) {
		ds.league_overview.init();
		
		// set up navigation
		ds.league_nav.init({
			menu: $('#league-menu-options')
		});
	}




	// set some page settings
	ds.height = $(document).height();
	ds.width = $(document).width();


	ds.nav.init({
	  nav: '#nav-menu',
	  toggle: '#nav-toggle',
	  search: '#search-li',
	});
});






ds.league_nav = (function() {
	// vars
	var menu = [], menuListener,
			current = 0, // index
			$root = $('html, body');


	// init
	var init = function(settings) {
		// set it up
		menuSetup(settings.menu);

		// do it up
		update();
	}

	var menuSetup = function(_menu) {
		// event listener
		menuListener = _menu;
		menuListener.on('click', function(e) {
			if (e.target.localName === 'a') {
				e.preventDefault();
				update(e.target);
			}
		});

		// populate array
		menu = $.makeArray(menuListener.find('a'));
	}

	var scrollToTop = function(_href) {
		// scroll to
		$root.animate({
			scrollTop: $(_href).offset().top
		}, 1000, function() {
			window.location.hash = _href;
		});
	}

	var update = function(_navItem) {
		// change class
		menuListener.find('.current').removeClass('current');

		// find nav selection
		if (_navItem) {
			for (var i = 0; i < menu.length; i++) {
				if (menu[i].attributes['href'].nodeValue.split('#')[1] === _navItem.attributes['href'].nodeValue.split('#')[1]) current = i;
			};
			scrollToTop(menu[current].attributes['href'].nodeValue);
		}

		// add class
		$(menu[current]).addClass('current');
	}

	return {
		init: init
	}
})();



ds.league_overview = (function() {

	// vars
	var league,
			clubs,
			current_club = {},
			stadium_overviews,
			table,
			table_rows,
			map,
			markers = [];

	// do it 2 it
	var init = function() {

		// DOM references
		// ===================================
		league = $('#league-overview');
		clubs = $.makeArray(league.children('.league-clubs').children());
		current_club.name = league.attr('data-current-club');
		stadium_overviews = $.makeArray(league.find('#stadium-overviews').children().children());
		table = league.find('.league-table');
		table_rows = $.makeArray(table.children('tbody').children());



		// map markers
		// ===================================
		for (var i = 0; i < stadium_overviews.length; i++) {
			// use data-attributes on the '.stadium' element
			var data = $(stadium_overviews[i]).find('.stadium');
			
			// push each club's data
			markers.push({
		    type: 'Feature',
		    geometry: {
		        type: 'Point',
		        coordinates: [data.attr('data-stadium-long'), data.attr('data-stadium-lat')]
		    },
		    properties: {
		        title: data.attr('data-stadium-name'),
		        // description: data.attr('data-stadium-address'),
		        'marker-size': 'small',
		        'marker-color': '#ADADAD',
		        club: stadium_overviews[i].getAttribute('data-club'),
		        index: i
		    }
			});
		};
		// initialize marker
		current_club.marker = markers[0];


		// i'm the map
		map = L.mapbox.map('map', 'examples.map-20v6611k');




		// add event listeners
		// ===================================
		// list of teams
		league.children('.league-clubs').on('click', function(e) {
			// get data attr
			if (e.target.localName === 'li') {
				current_club.name = $(e.target).attr('data-club');
			} else if (e.target.localName === 'img') {
				current_club.name = $(e.target.parentNode).attr('data-club');
			}
			// 
			update();
		});

		// league table
		table.on('click', function(e) {
			var test = $(e.target.parentNode).attr('data-club');
			if (test !== undefined) {
				current_club.name = test;
			}
			// 
			update();
		});

		// map markers
		map.markerLayer.on('click',function(e) {
			if(current_club.name === e.layer.feature.properties.club) {
				map.setView(e.latlng, map.getZoom() + 2);
			} else {
				current_club.name = e.layer.feature.properties.club;
				// 
				update();
			}
		});

		// map.on('click', console.log(map.getZoom()));
		// do it up
		// ===================================
		update();
	}


	var clearClasses = function() {
		$(current_club.node).removeClass('current');
		$(current_club.table).removeClass('current');
		$(current_club.overview).removeClass('current');	
	}


	var updateClasses = function() {
		$(current_club.node).addClass('current');
		$(current_club.table).addClass('current');
		$(current_club.overview).addClass('current');
	}


	var updateReferences = function() {
		// go through our elements and find the team to show
		for (var i = 0; i < clubs.length; i++) {
			// get DOM node
			if (clubs[i].getAttribute('data-club') === current_club.name) current_club.node = clubs[i];
			// table node
			if(table_rows[i].getAttribute('data-club') === current_club.name) current_club.table = table_rows[i];
			// overview node
			if (stadium_overviews[i].getAttribute('data-club') === current_club.name) current_club.overview = stadium_overviews[i];
			// marker
			if (markers[i].properties.club === current_club.name) current_club.marker = markers[i];
		};		
	}


	var updateMap = function() {
		
		var zoomLvl = 6;
		if (map.getZoom() >= 8) zoomLvl = map.getZoom(); 

		var newMap = $(current_club.overview).find('.stadium');
		map.setView([newMap.attr('data-stadium-lat'), newMap.attr('data-stadium-long')], zoomLvl);	

		// change colors
		resetColors();

		current_club.marker.properties['old-color'] = current_club.marker.properties['marker-color'];
		current_club.marker.properties['marker-color'] = '#000';
		
		// redraw markers
		map.markerLayer.setGeoJSON(markers);		
	}


	var resetColors = function(e) {
		for (var i = 0; i < markers.length; i++) {
			markers[i].properties['marker-color'] = markers[i].properties['old-color'] ||
			markers[i].properties['marker-color'];
		}
		// map.markerLayer.setGeoJSON(markers);
	}


	var update = function() {

		clearClasses();

		updateReferences();

		updateClasses();

		updateMap();
	}

	return {
		init: init
	}

})();