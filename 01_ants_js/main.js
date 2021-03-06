window.onload = function() {

// Globals
var antList;
var foodList;
var coarseMap;

/********************
 * Phaser functions *
 ********************/
function preload() {
  game.load.image('ant', 'assets/ant.png');
}

function create() {
  foodList = [];
  antList = [];
  spawnInitAnts(INIT_NUM_OF_ANTS);
  //spawnInitFood()
  //spawnInitDirt()
  
  // register input event handlers
  for (var i = 0; i < Math.min(10, FACTION.NUM); i++) {
    var key = game.input.keyboard.addKey(Phaser.Keyboard[dig2eng[(i + 1) % 10]]);
    // i'll explain this later
    (function(i) {
      key.onDown.add(function() {
        spawnAnt(i, [game.input.x, game.input.y])
      }, this);
    })(i);
  }

}

function update() {
  antList.forEach(function(ant) {
    //ant.checkSurroundings();
    //ant.decide();
    //ant.act();
  });
}

function render() {

}

var game = new Phaser.Game(GAME_WIDTH, GAME_HEIGHT, Phaser.AUTO, 'ants',
    { preload: preload, create: create, update: update, render: render });

/************************
 * Our helper functions *
 ************************/

function randRange(r) { return Math.floor(Math.random() * r); }
var randX = function() { return randRange(GAME_WIDTH) };
var randY = function() { return randRange(GAME_HEIGHT) };

function spawnInitAnts(x) {
  for (var i = 0; i < FACTION.NUM; i++) {
    var loc = [randX(), randY()];
    for (var j = 0; j < x/3; j++) { 
      spawnAnt(i, loc);
    }
  }
}

function spawnAnt(faction, loc) {
  var sprite = game.add.sprite(loc[0], loc[1], 'ant');
  var rgb = FACTION.COLORS[faction];
  sprite.tint = rgb[0] << 16 | rgb[1] << 8 | rgb[2];
  antList.push(new Ant(undefined, loc, undefined, 
        undefined, undefined, undefined, faction, undefined, sprite));
}



};

/*
  var help = game.add.text(16, 16, 'Arrows to scroll', 
      { font: '14px Arial', fill: '#ffffff' });
  help.fixedToCamera = true;
*/
