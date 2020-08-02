class FARule {
  constructor(public readonly state: number, public readonly character: string, public readonly nextState: number) {}

  public applyTo(state: number, character: string) {
    return this.state === state && this.character === character;
  }
}

class DFARuleBook {
  constructor(public readonly rules: Array<FARule>) {}

  public nextState(state: number, character: string) {
    return this.ruleFor(state, character)?.nextState;
  }

  public ruleFor(state: number, character: string) {
    for (const rule of this.rules) {
      if (rule.applyTo(state, character)) {
        return rule;
      }
    }
  }
}

class DFA {
  constructor(
    public currentState: number,
    public readonly acceptStates: Array<number>,
    public readonly ruleBook: DFARuleBook
  ) {}

  public accepting() {
    return this.acceptStates.includes(this.currentState);
  }

  public readCharacter(character: string) {
    this.currentState = this.ruleBook.nextState(this.currentState, character) || -1;
  }

  public readString(s: string) {
    for (const char of s) {
      this.readCharacter(char);
    }
  }
}

class DFADesign {
  constructor(public startState: number, public acceptStates: Array<number>, public readonly ruleRook: DFARuleBook) {}

  public toDfa() {
    return new DFA(this.startState, this.acceptStates, this.ruleRook);
  }

  public accepts(s: string) {
    const dfa = this.toDfa();
    dfa.readString(s);
    return dfa.accepting();
  }
}

const ruleBook = new DFARuleBook([
  new FARule(1, "a", 2),
  new FARule(1, "b", 1),
  new FARule(2, "a", 2),
  new FARule(2, "b", 3),
  new FARule(3, "a", 3),
  new FARule(3, "b", 3),
]);

console.log(ruleBook.nextState(1, "a"));
console.log(ruleBook.nextState(1, "b"));
console.log(ruleBook.nextState(2, "b"));

const dfa = new DFA(1, [3], ruleBook);
console.log(dfa.accepting());
dfa.readString("baaab");
console.log(dfa.accepting());

const dfaDesign = new DFADesign(1, [3], ruleBook);
console.log(dfaDesign.accepts("a"));
console.log(dfaDesign.accepts("baa"));
console.log(dfaDesign.accepts("baba"));
