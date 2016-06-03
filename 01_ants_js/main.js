window.onload = function() {

// Globals
var antList;
var foodList;

/********************
 * Phaser functions *
 ********************/
function preload() {
  game.load.image('ant', 'assets/brick.png');
}

function create() {
  foodList = [];
  antList = [];
  spawnInitAnts(INIT_NUM_OF_ANTS);
  //spawnInitFood()
  //spawnInitDirt()
}

function update() {
  spawnAnts();
  //spawnFood();
  //spawnDirt();

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

function spawnAnts() {
  if (game.input.keyboard.isDown(Phaser.Keyboard.LEFT)) {
    var faction = randint(0, FACTION.NUM);
    spawnAnt(faction, [game.input.x, game.input.y]);
  }
  for (var i = 0; i < 10; i++) {
    var key = dig2eng[(i + 1) % 10];
    if (eval("game.input.keyboard.isDown(Phaser.Keyboard." + key + ")")) {
      spawnAnt(i, [game.input.x, game.input.y]);
    }
  }
}


};

/*
  var help = game.add.text(16, 16, 'Arrows to scroll', 
      { font: '14px Arial', fill: '#ffffff' });
  help.fixedToCamera = true;
*/
