
function ProjectsController($scope) {
  this.scope_ = $scope;
  this.scope_.projects = [
  {
    title: 'The AlgoRedis Challenge',
    link: 'https://levelup.gitconnected.com/sharpen-your-redis-skills-with-the-algoredis-challenge-01f64fa5da84',
    thumbnail: '/imgs/algoredis.png',
    description: 'Sharpen your Redis skills with an algorithms challenge.',
    tags: ['Redis', 'Python', 'Medium', 'Algorithms'],
    links: [{
      title: 'Medium',
      link: 'https://levelup.gitconnected.com/sharpen-your-redis-skills-with-the-algoredis-challenge-01f64fa5da84'
    }, {
      title: 'Source',
      link: 'https://github.com/pbaumstarck/algoredis'
    }, {
      title: 'Level Up Coding',
      link: 'https://levelup.gitconnected.com/'
    }]
  }, {
    title: 'Han Solo’s Guide to C++ Casting',
    link: 'https://betterprogramming.pub/han-solos-guide-to-c-casting-344043d90030',
    thumbnail: '/imgs/han_solo_casting.png',
    description: 'Clear your C++ cast concepts with Star Wars.',
    tags: ['C++', 'Medium',],
    links: [{
      title: 'Medium',
      link: 'https://betterprogramming.pub/han-solos-guide-to-c-casting-344043d90030'
    }, {
      title: 'Better Programming',
      link: 'https://betterprogramming.pub/'
    }]
  }, {
    title: 'Programming Puzzle: Tic-Tac-Toe Keychain',
    link: 'https://thepgb.medium.com/programming-puzzle-tic-tac-toe-keychain-e247cc8c4ec7',
    thumbnail: '/imgs/tic_tac_toe_keychain.png',
    description: 'Another programming exercise with a simple game.',
    tags: ['Python', 'Medium', 'Algorithms'],
    links: [{
      title: 'Medium',
      link: 'https://thepgb.medium.com/programming-puzzle-tic-tac-toe-keychain-e247cc8c4ec7'
    }, {
      title: 'Source',
      link: 'https://github.com/pbaumstarck/scaling-invention/blob/main/code/tic_tac_toe.py'
    }]
  }, {
    title: 'Simple Python Parsing for Narrative Charts',
    link: 'https://betterprogramming.pub/simple-python-parsing-for-narrative-charts-37e51c75ca3d',
    thumbnail: '/imgs/narrative_charts.png',
    description: 'Creating visualizations for books.',
    tags: ['Visualization', 'Medium',],
    links: [{
      title: 'Medium',
      link: 'https://betterprogramming.pub/simple-python-parsing-for-narrative-charts-37e51c75ca3d'
    }, {
      title: 'Better Programming',
      link: 'https://betterprogramming.pub/'
    }]
  }, {
    title: 'Programming Puzzle: Speedrunning Ticket to Ride',
    link: 'https://levelup.gitconnected.com/programming-puzzle-speedrunning-ticket-to-ride-ae044e724357',
    thumbnail: '/imgs/ticket_to_ride_speedrun.png',
    description: 'Finding the fastest possible win on the popular board game.',
    tags: ['Game-playing', 'Graphs', 'Search', 'Medium',],
    links: [{
      title: 'Medium',
      link: 'https://levelup.gitconnected.com/programming-puzzle-speedrunning-ticket-to-ride-ae044e724357'
    }, {
      title: 'Level Up Coding',
      link: 'https://levelup.gitconnected.com/'
    }]
  }, {
    title: 'Programming Puzzle: Ticket to Ride First Journey',
    link: 'https://thepgb.medium.com/programming-puzzle-ticket-to-ride-first-journey-ba72d4594f1e',
    thumbnail: '/imgs/ticket_to_ride.png',
    description: 'Graph algorithms on the popular board game.',
    tags: ['Game-playing', 'Graphs', 'Search', 'Medium',],
    links: [{
      title: 'Medium',
      link: 'https://thepgb.medium.com/programming-puzzle-ticket-to-ride-first-journey-ba72d4594f1e'
    }]
  }, {
    title: 'Programming Puzzle: Lights Out',
    link: 'https://medium.com/swlh/programming-puzzle-lights-toggle-f4d27bf3683e',
    thumbnail: '/imgs/lights_out.png',
    description: 'Exhaustive search on a simple puzzle game.',
    tags: ['Game-playing', 'Search', 'Medium',],
    links: [{
      title: 'Medium',
      link: 'https://medium.com/swlh/programming-puzzle-lights-toggle-f4d27bf3683e'
    }, {
      title: 'The Startup',
      link: 'https://medium.com/swlh'
    }]
  }, {
    title: 'Nyan Bars',
    link: '/nyan_bars.html',
    thumbnail: '/imgs/nyan_bars.png',
    description: 'jQuery plugin for animated text progress bars you can ' +
                 'build with a custom language.',
    tags: ['jQuery', 'Parsing', 'Progress Bars'],
    links: [{
      title: 'Demo',
      link: '/nyan_bars.html'
    }, {
      title: 'Source',
      link: 'https://github.com/pbaumstarck/jquery-nyan-bars'
    }]
  }, {
    title: 'ZSON – Bedizened JSON',
    link: '/zson.html',
    thumbnail: '/imgs/zson.png',
    description: 'JSON that supports comments, multi-line strings, ' +
                 'trailing commas, and readable numbers.',
    tags: ['Parsing', 'JSON', 'Productivity'],
    links: [{
      title: 'Demo',
      link: '/zson.html'
    }, {
      title: 'Source',
      link: 'https://github.com/pbaumstarck/ZSON'
    }]
  }, {
    title: 'CSS Solar System',
    link: '/solar_system.html',
    thumbnail: '/imgs/solar_system.png',
    description: 'A stylized solar system model made with LESS and designed ' +
                 'as a website header.',
    tags: ['CSS', 'LESS', 'Demos'],
    links: [{
      title: 'Demo',
      link: '/solar_system.html'
    }, {
      title: 'Source',
      link: 'http://jsfiddle.net/pbaumstarck/hfbq8/'
    }]
  }, {
    title: 'iOS Chess',
    link: 'https://github.com/pbaumstarck/iOS-Chess',
    thumbnail: '/imgs/ios_chess.png',
    description: 'Simple Chess app I built to get familiar with iOS development.',
    tags: ['iOS', 'Chess', 'Mobile'],
    links: [{
      title: 'Source',
      link: 'https://github.com/pbaumstarck/iOS-Chess'
    }]
  }];

  // this.scope_.tagCount = 0;
  this.scope_.tags = {};
  this.scope_.toggleTag = _.bind(this.toggleTag, this);
  this.scope_.filterProject = _.bind(this.filterProject, this);
  this.scope_.isTagOn = _.bind(this.isTagOn, this);
  this.scope_.isAnyTagOn = _.bind(this.isAnyTagOn, this);
  this.scope_.clearAllTags = _.bind(this.clearAllTags, this);

  this.scope_.tagCount = _.bind(function() {
    return _.reduce(_.values(this.scope_.tags), function(a, b) {
      return a + (b ? 1 : 0);
    }, 0);
  }, this);
}


ProjectsController.prototype.toggleTag = function(tag) {
  if (!(tag in this.scope_.tags)) {
    this.scope_.tags[tag] = false;
  }
  this.scope_.tags[tag] = !this.scope_.tags[tag];
};


ProjectsController.prototype.isTagOn = function(tag) {
  return this.scope_.tags[tag] === true;
};


ProjectsController.prototype.isAnyTagOn = function(tag) {
  for (var key in this.scope_.tags) {
    if (this.scope_.tags[key]) {
      return true;
    }
  }
  return false;
};


ProjectsController.prototype.filterProject = function(project) {
  if (!this.scope_.tagCount()) {
    return true;
  }
  return _.reduce(_.map(project.tags, function(tag) {
    return this.scope_.tags[tag] ? 1 : 0;
  }, this), function(a, b) { return a + b; }, 0, this) ==
      this.scope_.tagCount();
};


ProjectsController.prototype.clearAllTags = function() {
  for (var key in this.scope_.tags) {
    this.scope_.tags[key] = false;
  }
};
