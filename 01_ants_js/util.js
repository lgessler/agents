function randint (lb, ub) {
  return Math.floor((Math.random() * (ub - lb)) + lb);
}

// ugh 
var dig2eng = {
  0: "ZERO",
  1: "ONE",
  2: "TWO",
  3: "THREE",
  4: "FOUR",
  5: "FIVE",
  6: "SIX",
  7: "SEVEN",
  8: "EIGHT",
  9: "NINE"
};

// http://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript
function get_id() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
    return v.toString(16);
  });
}
