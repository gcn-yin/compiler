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
