/**
 * recognize "r[0-9]+", represent 'register name'
 */
class TableDrivenScanner {
  /**
   * @param {string[]} input
   */
  constructor(input) {
    this.sa = ["s2"];
    this.se = "se";
    this.register = ["r"];
    this.digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
    this.stack = [];
    this.pointer = 0;
    this.input = input;
    this.current = null;
    this.charCat = {
      r: "register",
      number: "digit",
      eof: "other",
      other: "other"
    };
    this.typeTable = {
      s0: "invalid",
      s1: "invalid",
      s2: "register",
      se: "invalid"
    };
    this.transformTable = {
      s0: { register: "s1", digit: "se", other: "se" },
      s1: { register: "se", digit: "s2", other: "se" },
      s2: { register: "se", digit: "s2", other: "se" },
      se: { register: "se", digit: "se", other: "se" }
    };
  }

  nextChar() {
    let result = this.input[this.pointer];
    this.pointer++;
    return result;
  }

  rollback() {
    let result = this.input[this.pointer];
    this.pointer--;
    return result;
  }

  /**
   * @param {string} char
   */
  _charCat(char) {
    if (this.digit.includes(char)) {
      return "digit";
    } else if (char === "r") {
      return "register";
    } else {
      return "other";
    }
  }

  nextWord() {
    let state = "s0";
    let lexeme = [];
    this.stack = [];
    this.stack.push("bad");
    while (state !== this.se) {
      let char = this.nextChar();
      lexeme.push(char);
      if (this.sa.includes(state)) {
        this.stack = [];
      }
      this.stack.push(state);
      let cat = this._charCat(char);
      state = this.transform(state, cat);
    }
    while (!this.sa.includes(state) && state !== "bad") {
      state = this.stack.pop();
      lexeme.pop();
      this.rollback();
    }
    if (this.sa.includes(state)) {
      return this.typeTable[state];
    }
    return "invalid";
  }

  transform(state, cat) {
    return this.transformTable[state][cat];
  }
}

let p = new TableDrivenScanner("r123");
console.log(p.nextWord());

module.exports = {};
