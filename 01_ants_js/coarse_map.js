var Map = function() {
  this.rows =    GAME_WIDTH  / COARSE_MAP_EDGE_SIZE;
  this.columns = GAME_HEIGHT / COARSE_MAP_EDGE_SIZE;
  this.map = {};
};

function initCell(x, y) {
  if (this.map[index] === undefined) {
    this.map[index] = [];
  }
}

Map.prototype = {
  get: function(x, y) {
    var index = x*y + y;
    initCell(x, y);
    return this.map[index];
  },
  add: function(ant, x, y) {
    var index = x*y + y;
    initCell(x, y);
    this.map[index].push(ant);
  },
  remove: function(ant, x, y) {
    var index = x*y + y;
    initCell(x, y);
    this.map[index] = this.map[index].filter(function(otherAnt) {
      otherAnt._id !== ant._id;  
    });
  }
};
