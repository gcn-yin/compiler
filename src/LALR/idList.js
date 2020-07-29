/**
 * 2019-01-28
 * practice LALR parser
 */

class IdList {
  constructor(id, idListTail) {
    this.id = id;
    this.idListTail = idListTail;
  }
}

class IdListTail {
  constructor(id = undefined, idListTail = undefined) {
    if (id && idListTail) {
      this.id = id;
      this.idListTail = idListTail;
    }
  }
}

function isLetter(c) {
  return c.toLowerCase() !== c.toUpperCase();
}

class Parser {
  /**
   * bnf of id_list:
   *
   * id_list ::= id id_list_tail
   *
   * id_list_tail ::= , id_list_tail
   *
   * id_list_tail ::= ;
   *
   * example: "a, b, c;"
   * @param {string[]} tokens
   */
  constructor(tokens) {
    this.tokens = tokens;
    /** @type {number} */ this.pointer = tokens.length - 1;
    /** @type {string} */ this.current = tokens[this.pointer];
    this.currentState = null;
  }

  moveLeft() {
    this.pointer--;
    this.current = this.tokens[this.pointer];
  }

  moveRight() {
    this.pointer++;
    this.current = this.tokens[this.pointer];
  }

  term() {
    if (this.current === ";") {
      this.currentState = new IdListTail();
      this.moveLeft();
      return this.currentState;
    }
    const tail = this.currentState;
    if (tail instanceof IdListTail) {
      const id = this.current;
      if (isLetter(id)) {
        this.moveLeft();
        if (this.current === ",") {
          this.currentState = new IdListTail(id, tail);
          this.moveLeft();
          return this.currentState;
        }
        return new IdList(id, tail);
      }
    }
  }

  idList() {
    let result;
    while (this.current) {
      result = this.term();
    }
    return result;
  }
}

const tokens = ["a", ",", "b", ",", "c", ",", "d", ";"];

const p = new Parser(tokens);

console.log(p.idList());

module.exports = {};
