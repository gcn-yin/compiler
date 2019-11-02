interface IRule {
    accept(input: string): { contain: boolean, groups: IGroup[] };
}

interface IGroup {
    getGroups(): string | IGroup[];
}

class Group implements IGroup {
    protected constructor(private readonly groups: IGroup[]) { }

    public static of(...groups: IGroup[]) {
        return new Group(groups);
    }

    public getGroups() {
        return this.groups;
    }
}

class RawTextGroup implements IGroup {
    protected constructor(private readonly text: string) { }

    public static of(text: string) {
        return new RawTextGroup(text);
    }

    public getGroups() {
        return this.text;
    }
}

class RawTextRule implements IRule {
    protected constructor(private readonly text: string) { }

    public static of(text: string): IRule {
        return new RawTextRule(text);
    }

    public accept(input: string) {
        return { contain: input.startsWith(this.text), groups: [RawTextGroup.of(this.text)] };
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
        return { contain, groups: [RawTextGroup.of(capturedText)] };
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
        const temp = input;
        const groups: IGroup[] = [];
        let i = 0;
        for (; i < this.times; i++) {
            const { contain: _c, groups: _g } = this.rule.accept(temp);
            if (_c) {
                groups.push(Group.of(..._g));
            } else {
                break;
            }
        }
        const contain = this.times <= i;
        return { contain, groups };
    }
}

const rule = TimesRule.of(3, RawTextRule.of('haha '));
console.log(rule.accept('haha haha haha '));

const rule2 = RawTextRule.of('lalala');
console.log(rule2.accept('lalala'))
