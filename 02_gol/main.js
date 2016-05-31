/**
 * Lightly modified version of yanisvieilly/game-of-life
 */
window.onload = function() {

  // declare constants
  var WIDTH = 800;
  var HEIGHT = 600;

  var CELL_COLUMNS = WIDTH / 10;
  var CELL_ROWS = HEIGHT / 10;

  // declare here so more than one function can see it
  var cells;

  function createCells() {

    // this is what a cell looks like: tell the game it is 10px x 10px, then
    // make it black 
    var cellBitmap = game.add.bitmapData(10, 10);
    cellBitmap.fill(0x00, 0x00, 0x00);

    // tell Phaser to think of cells as a group
    cells = game.add.group();

    // create the cells: the last parameter tells Phaser whether the entity
    // 'exists' or not 
    // phaser.io/docs/2.4.4/Phaser.Group.html#create
    for (var y = 0; y < CELL_ROWS; y++) {
      for (var x = 0; x < CELL_COLUMNS; x++) {
        // random
        //cells.create(x * 10, y * 10, cellBitmap, 0, 
        //    game.rnd.between(0, 20) === 10);
        // glider spaceship
        cells.create(x * 10, y * 10, cellBitmap, 0,
            (y === 0 && x === 2) || (y === 1 && x === 0) || (y === 1 && x === 2) 
            || (y === 2 && x === 1) || (y === 2 && x === 2));
      }
    }
  }

  // this function is called by Phaser
  function create() {
    game.stage.backgroundColor = 0xFFFFFF;
    
    createCells();

    // use Phaser's internal clock to decide how often to update
    game.time.events.loop(Phaser.Timer.HALF, updateCells, this);
  }

  function getNeighborPositions(cellIndex) {
    return [
      cellIndex - CELL_COLUMNS - 1,
      cellIndex - CELL_COLUMNS,
      cellIndex - CELL_COLUMNS + 1,
      cellIndex - 1,
      cellIndex + 1,
      cellIndex + CELL_COLUMNS - 1,
      cellIndex + CELL_COLUMNS,
      cellIndex + CELL_COLUMNS + 1
    ];
  }

  function getLivingNeighbors(cell) {
    var quantity = 0;
    var neighborPositions = getNeighborPositions(cell.z);

    for (var i = 0; i < neighborPositions.length; i++) {
      var pos = neighborPositions[i];
      if (cells.getAt(pos) && cells.getAt(pos).alive) {
        // --> GOL doesn't care if you have more than 4 living neighbors?
        if (++quantity === 4) {
          break;
        }
      }
    }
    return quantity;
  }

  function updateCells() {
    var toBeKilled = [];
    var toBeReset = [];

    cells.children.forEach(function(cell) {
      var aliveNeighbors = getLivingNeighbors(cell);

      if (cell.alive && aliveNeighbors !== 2 && aliveNeighbors !== 3) {
        toBeKilled.push(cell)
      }
      else if (aliveNeighbors === 3) {
        toBeReset.push(cell); 
      }
    });

    killOrResetCells(toBeKilled, toBeReset);
  }

  function killOrResetCells(toBeKilled, toBeReset) {
    toBeKilled.forEach(function(cell) { cell.kill() });
    toBeReset.forEach(function(cell) { cell.reset(cell.x, cell.y) });
  }


  // make a new 800x600 game, use the function we defined create to create the
  // game
  game = new Phaser.Game(800, 600, Phaser.AUTO, '', {create: create});

};


