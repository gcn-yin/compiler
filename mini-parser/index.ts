interface IRule {
    accept(input: string): { contain: boolean, groups: IGroup[] };
}

interface IGroup {
    getGroups(): string | IGroup[];
    toRawString(): string;
}

class TreeGroup implements IGroup {
    protected constructor(private readonly groups: IGroup[]) { }

    public static of(...groups: IGroup[]) {
        return new TreeGroup(groups);
    }

    public getGroups() {
        return this.groups;
    }

    public toRawString() {
        return this.groups.map(g => g.toRawString()).join("");
    }
}

class LeafGroup implements IGroup {
    protected constructor(private readonly text: string) { }

    public static of(text: string) {
        return new LeafGroup(text);
    }

    public getGroups() {
        return this.text;
    }

    public toRawString() {
        return this.text;
    }
}

class RawTextRule implements IRule {
    protected constructor(private readonly text: string) { }

    public static of(text: string): IRule {
        return new RawTextRule(text);
    }

    public accept(input: string) {
        return { contain: input.startsWith(this.text), groups: [LeafGroup.of(this.text)] };
    }
}

class RegExpRule implements IRule {
    private readonly regExp: RegExp;

    protected constructor(regExp: string | RegExp) {
        this.regExp = new RegExp(regExp);
    }

    public static of(regExp: string | RegExp): IRule {
        return new RegExpRule(regExp);
    }

    public accept(input: string) {
        const regExpExecArray = this.regExp.exec(input);
        const contain = regExpExecArray ? regExpExecArray.index === 0 : false;
        const capturedText = regExpExecArray ? regExpExecArray[0] : '';
        return { contain, groups: [LeafGroup.of(capturedText)] };
    }
}

class TimesRule implements IRule {
    protected constructor(private readonly times: number, private readonly rule: IRule) { }

    /**
     * times should >= 0
     * if you pass a number that < 0
     * rule will accept it as 0
     */
    public static of(times: number, rule: IRule): IRule {
        return new TimesRule(times, rule);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let i = 0;
        for (; i < this.times; i++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(..._g));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            } else {
                break;
            }
        }
        const contain = this.times <= i;
        return { contain, groups };
    }
}

class OneOrMoreRule implements IRule {
    protected constructor(private readonly rule: IRule) { }

    public static of(rule: IRule): IRule {
        return new OneOrMoreRule(rule);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let count = 0;
        for (; temp !== ''; count++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(..._g));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            } else {
                break;
            }
        }
        const contain = count > 0;
        return { contain, groups };
    }
}

class ZeroOrMoreRule implements IRule {
    protected constructor(private readonly rule: IRule) { }

    public static of(rule: IRule): IRule {
        return new ZeroOrMoreRule(rule);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let count = 0;
        for (; temp !== '' ; count++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(..._g));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            } else {
                break;
            }
        }
        return { contain: true, groups };
    }
}

class AndRule implements IRule {
    protected constructor(private readonly rules: IRule[]) { }

    public static of(...rules: IRule[]) {
        return new AndRule(rules);
    }

    public accept(input: string) {
        let count = 0;
        let temp = input;
        const groups: IGroup[] = []
        for (let rule of this.rules) {
            const { contain, groups: _g } = rule.accept(temp);
            if (contain) {
                groups.push(TreeGroup.of(..._g));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
                count++;
            } else {
                break;
            }
        }
        const contain = count === this.rules.length;
        return { contain, groups };
    }
}

class OrRule implements IRule {
    protected constructor(private readonly rules: IRule[]) { }

    public static of(...rules: IRule[]) {
        return new OrRule(rules);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let contain = false;
        for (let rule of this.rules) {
            const { contain: _c, groups: _g } = rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(..._g));
                contain = true;
                break;
            } else {
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            }
        }
        return { contain, groups };
    }
}

class AnyCharRule implements IRule {
    protected constructor() { }

    public static of() {
        return new AnyCharRule();
    }

    public accept(input: string) {
        const contain = input.length > 0;
        const groups: IGroup[] = contain ? [LeafGroup.of(input[0])] : [];
        return { contain, groups };
    }
}

const rule1 = TimesRule.of(3, RawTextRule.of('haha '));
console.log(rule1.accept('haha haha haha '));

const rule2 = RawTextRule.of('lalala');
console.log(rule2.accept('lalala'));

const rule3 = OneOrMoreRule.of(RawTextRule.of("la"));
console.log(rule3.accept('lalalala'));

const rule4 = AndRule.of(RawTextRule.of("hello"), RawTextRule.of(" world!"));
console.log(rule4.accept("hello world!"));

const rule5 = AndRule.of(
    OneOrMoreRule.of(RawTextRule.of('la')),
    ZeroOrMoreRule.of(RawTextRule.of("fuck")),
    OrRule.of(RawTextRule.of("!"), RawTextRule.of("?")));
console.log(rule5.accept("lalalafuck?"));
