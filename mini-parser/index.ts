interface IRule {
    getName(): string | null | undefined;
    accept(input: string): { contain: boolean, groups: IGroup[] };
}

interface IGroup {
    getName(): string | null | undefined;
    getSubGroups(): IGroup[];
    toRawString(): string;
}

class TreeGroup implements IGroup {
    protected constructor(private readonly groups: IGroup[], private readonly name: string | null | undefined = null) { }

    public static of(groups: IGroup[], name: string | null | undefined = null): IGroup {
        return new TreeGroup(groups, name);
    }

    public getSubGroups() {
        return this.groups;
    }

    public toRawString() {
        return this.groups.map(g => g.toRawString()).join("");
    }

    public getName() {
        return this.name;
    }
}

class LeafGroup implements IGroup {
    protected constructor(private readonly text: string, private readonly name: string | null | undefined = null) { }

    public static of(text: string, name: string | null | undefined = null): IGroup {
        return new LeafGroup(text, name);
    }

    public getSubGroups() {
        return [];
    }

    public toRawString() {
        return this.text;
    }

    public getName() {
        return this.name;
    }
}

class RawTextRule implements IRule {
    protected constructor(private readonly text: string, private name: string | null | undefined = null) { }

    public static of(text: string, name: string | null | undefined = null): IRule {
        return new RawTextRule(text, name);
    }

    public accept(input: string) {
        return { contain: input.startsWith(this.text), groups: [LeafGroup.of(this.text)] };
    }

    public getName() {
        return this.name;
    }
}

class RegExpRule implements IRule {
    private readonly regExp: RegExp;

    protected constructor(regExp: string | RegExp, private readonly name: string | null | undefined = null) {
        this.regExp = new RegExp(regExp);
    }

    public static of(regExp: string | RegExp, name: string | null | undefined = null): IRule {
        return new RegExpRule(regExp);
    }

    public accept(input: string) {
        const regExpExecArray = this.regExp.exec(input);
        const contain = regExpExecArray ? regExpExecArray.index === 0 : false;
        const capturedText = regExpExecArray ? regExpExecArray[0] : '';
        return { contain, groups: [LeafGroup.of(capturedText, this.name)] };
    }

    public getName() {
        return this.name;
    }
}

class TimesRule implements IRule {
    protected constructor(private readonly times: number, private readonly rule: IRule, private readonly name: string | null | undefined = null) { }

    /**
     * times should >= 0
     * if you pass a number that < 0
     * rule will accept it as 0
     */
    public static of(times: number, rule: IRule, name: string | null | undefined = null): IRule {
        return new TimesRule(times, rule, name);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let i = 0;
        for (; i < this.times; i++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(_g, this.name));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            } else {
                break;
            }
        }
        const contain = this.times <= i;
        return { contain, groups };
    }

    public getName() {
        return this.name;
    }
}

class OneOrMoreRule implements IRule {
    protected constructor(private readonly rule: IRule, private readonly name: string | null | undefined = null) { }

    public static of(rule: IRule, name: string | null | undefined = null): IRule {
        return new OneOrMoreRule(rule, name);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let count = 0;
        for (; temp !== ''; count++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(_g, this.name));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            } else {
                break;
            }
        }
        const contain = count > 0;
        return { contain, groups };
    }

    public getName() {
        return this.name;
    }
}

class ZeroOrMoreRule implements IRule {
    protected constructor(private readonly rule: IRule, private readonly name: string | null | undefined = null) { }

    public static of(rule: IRule, name: string | null | undefined = null): IRule {
        return new ZeroOrMoreRule(rule, name);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let count = 0;
        for (; temp !== '' ; count++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(_g, this.name));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            } else {
                break;
            }
        }
        return { contain: true, groups };
    }

    public getName() {
        return this.name;
    }
}

class AndRule implements IRule {
    protected constructor(private readonly rules: IRule[], private readonly name: string | null | undefined = null) { }

    public static of(rules: IRule[], name: string | null | undefined = null) {
        return new AndRule(rules, name);
    }

    public accept(input: string) {
        let count = 0;
        let temp = input;
        const groups: IGroup[] = []
        for (let rule of this.rules) {
            const { contain, groups: _g } = rule.accept(temp);
            if (contain) {
                groups.push(TreeGroup.of(_g, this.name));
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
                count++;
            } else {
                break;
            }
        }
        const contain = count === this.rules.length;
        return { contain, groups };
    }

    public getName() {
        return this.name;
    }
}

class OrRule implements IRule {
    protected constructor(private readonly rules: IRule[], private readonly name: string | null | undefined = null) { }

    public static of(rules: IRule[], name: string | null | undefined = null) {
        return new OrRule(rules, name);
    }

    public accept(input: string) {
        let temp = input;
        const groups: IGroup[] = [];
        let contain = false;
        for (let rule of this.rules) {
            const { contain: _c, groups: _g } = rule.accept(temp);
            if (_c) {
                groups.push(TreeGroup.of(_g, this.name));
                contain = true;
                break;
            } else {
                temp = temp.replace(_g.map(g => g.toRawString()).join(""), '');
            }
        }
        return { contain, groups };
    }

    public getName() {
        return this.name;
    }
}

class AnyCharRule implements IRule {
    protected constructor(private readonly name: string | null | undefined = null) { }

    public static of(name: string | null | undefined = null) {
        return new AnyCharRule(name);
    }

    public accept(input: string) {
        const contain = input.length > 0;
        const groups: IGroup[] = contain ? [LeafGroup.of(input[0], this.name)] : [];
        return { contain, groups };
    }

    public getName() {
        return this.name;
    }
}

const rule1 = TimesRule.of(3, RawTextRule.of('haha '));
console.log(rule1.accept('haha haha haha '));

const rule2 = RawTextRule.of('lalala');
console.log(rule2.accept('lalala'));

const rule3 = OneOrMoreRule.of(RawTextRule.of("la"));
console.log(rule3.accept('lalalala'));

const rule4 = AndRule.of([
    RawTextRule.of("hello"),
    RawTextRule.of(" world!")
]);
console.log(rule4.accept("hello world!"));

const rule5 = AndRule.of([
    OneOrMoreRule.of(RawTextRule.of('la'), 'LA'),
    ZeroOrMoreRule.of(RawTextRule.of("fuck"), "FUCK"),
    OrRule.of([RawTextRule.of("!", "!!!"), RawTextRule.of("?", "WHAT")], "OR_SAMBLE")
], 'AND_RULE');
console.log(JSON.stringify(rule5.accept("lalalafuck?")));
