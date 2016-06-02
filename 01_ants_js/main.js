window.onload = function() {

var map, layer, cursors;

function preload() {
  game.load.tilemap('map', 'assets/map.json', null, Phaser.Tilemap.TILED_JSON);
};

function create() {
  map = game.add.tilemap('map', 16, 16);
  layer = map.createLayer(0);
  layer.resizeWorld();
  cursors = game.input.keyboard.createCursorKeys();

  var help = game.add.text(16, 16, 'Arrows to scroll', 
      { font: '14px Arial', fill: '#ffffff' });
  help.fixedToCamera = true;
};

function update() {
  if (cursors.left.isDown) {
    game.camera.x -= 4;
  } 
  else if (cursors.right.isDown) {
    game.camera.x += 4;
  }
  if (cursors.up.isDown) {
    game.camera.y -= 4;
  } 
  else if (cursors.down.isDown) {
    game.camera.y += 4;
  }
};

function render() {

};

var game = new Phaser.Game(800, 640, Phaser.AUTO, 'ants',
    { preload: preload, create: create, update: update, render: render });



};


