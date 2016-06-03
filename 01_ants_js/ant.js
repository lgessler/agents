// constructor
var Ant = function(name, position, health, damage, moveSpeed, digSpeed, faction, color, sprite) {
  if (this.name !== undefined) this.name = name;
  if (this.position !== undefined) this.position = position;
  if (this.health !== undefined) this.health = health;
  if (this.damage !== undefined) this.damage = damage;
  if (this.moveSpeed !== undefined) this.moveSpeed = moveSpeed;
  if (this.digSpeed !== undefined) this.digSpeed = digSpeed;
  if (this.faction !== undefined) this.faction = faction;
  this.color = FACTION.COLORS[this.faction];
  
  //assign sprite and sprite position
  this.sprite = sprite;
  this.sprite.x = position[0];
  this.sprite.y = position[1];
  
  this.friendlySurroundings = [];
  this.hostileSurroundings = [];
  this.state = "wander";
  this.antToAttack = null;
  this.squad = null; 
  this.foodSource = null; 
  this.digTarget = null; 
};

Ant.prototype = {
  name: (name !== undefined) ? name : (Math.random() < .5) ? "Antonius" : "Antonia",
  position: [randint(0, GAME_HEIGHT), randint(0, GAME_WIDTH)],
  state: "wander",
  health: randint(5, 40),
  damage: randint(2, 6),
  moveSpeed: randint(20, 35),
  digSpeed: randint(2, 3),
  faction: randint(0, FACTION.NUM),
  color: undefined // set this later
};

Ant.prototype.distanceTo = function(entity) {
  //return Manhattan distance between this and another entity
  if(entity === null)
    return POSITIVE_INFINITY;
  xDistance = abs(position[0] - entity.position[0]);
  yDistance = abs(position[1] - entity.position[1]);
  return xDistance + yDistance;
};

Ant.prototype.setColor = function() {
  //ensure that color of ant matches RGB faction. Unnecessary probably
  if(faction == "red") {
    color = [randint(0, 75) + 170, 0, 0];
  }
  if(faction == "green") {
    color = [0, randint(0, 75) + 170, 0];
  }
  
  if(faction == "blue") {
    color = [0, 0, randint(0, 75) + 170];
  }
};
  
Ant.prototype.setPos = function(position) {
  //need to update map accordingly
  position = position;
};

Ant.prototype.normalize = function(vector) {
  //normalize vector to unit length
  lengthSquared = vector[0] * vector[0] + vector[1] * vector[1];
  if(lengthSquared != 0) {
    length = sqrt(lengthSquared);
    vector[0] = vector[0] / length;
    vector[1] = vector[1] / length;
  }
  return vector
};

Ant.prototype.dig() = function() {
  digTarget.amount -= digSpeed * (1/60);
  if(digTarget.amount <= 0){
    digList.remove(digTarget);
    digTarget.sprite.kill();
    kill(digTarget);
    digTarget = null;
  }
};

Ant.prototype.move = function(moveVector) {
  moveVector = normalize(moveVector);
  position += moveVector * speed;
  
  if(position[0] < 0)
    position[0] = 0;
  if(position[0] > GAME_WIDTH - 1)
    position[0] = GAME_WIDTH - 1;
  if(position[1] < 0)
    position[1] = 0;
  if(position[1] > GAME_HEIGHT - 1)
    position[1] = GAME_HEIGHT - 1;
  
  sprite.x = position[0]
  sprite.y = position[1]
};

Ant.prototype.attack = function(target) {
  //attack a target
  target.health -= damage;
  if(target.health <= 0) {
    health += target.health / 2;
    damage += 1;
    hostileSurroundings.remove(target);
    target.sprite = null;
    antToAttack = null;
  }
};

Ant.prototype.attackMove = function() {
  moveVector = [antToAttack.position[0] - position[0], 
                antToAttack.position[1] - position[1]];
  move(moveVector);
};

Ant.prototype.eat = function() {
  if(foodSource.quantity <= 0) {
    foodSurroundings.remove(foodSource);
    foodSource = null;
  } else {
    foodSource.quantity -= (1/60);
    health += (1/60) * foodSource.quality;
    damage += (1/60) * foodSource.quality * .2;
  }
};

Ant.prototype.eatMove() = function(){
  moveVector = [foodSource.position[0] - position[0],
                foodSource.position[1] - position[1]];
  move(moveVector);
}
