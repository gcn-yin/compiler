interface ISource {
    getTokenList(): string[];
    addRule(...rule: IRule[]): ISource;
    accept(rule: IRule): void;
    parse(): void;
}

class Source implements ISource {
    private readonly tokenList: string[] = [];
    private readonly rules: IRule[] = [];

    public constructor(private content: string) { }

    public getTokenList() {
        return this.tokenList;
    }

    public addRule(...rule: IRule[]): ISource {
        this.rules.push(...rule);
        return this;
    }

    public parse() {
        for (let it of this.rules) {
            const { contain, capturedText } = it.tryParse(this.content);
            if (!contain) {
                break;
            }
            this.tokenList.push(capturedText);
            this.content = this.content.replace(capturedText, '');
        }
    }

    public accept(rule: IRule) {
        const { contain, capturedText } = rule.tryParse(this.content);
    }
}

interface IRule {
    visit(source: ISource): void;
    tryParse(input: string): { contain: boolean, capturedText: string };
}

class RawRule implements IRule {
    public constructor(private readonly rawText: string) {}

    public visit(source: ISource) {
        source.accept(this);
    }

    public tryParse(input: string) {
        const contain = input.startsWith(this.rawText);
        return { contain, capturedText: this.rawText };
    }
}

class RegExpRule implements IRule {
    private readonly regExp: RegExp;
    public constructor(regText: string) { 
        this.regExp = new RegExp(regText);
    }

    private startsWithRegExp(input: string) {
        const regExpExecArray = this.regExp.exec(input);
        const contain = regExpExecArray ? regExpExecArray.index === 0 : false;
        const capturedText = regExpExecArray ? regExpExecArray[0] : '';
        return { contain, capturedText };
    }

    public visit(source: ISource) {
        source.accept(this);
    }

    public tryParse(input: string) {
        const { contain, capturedText } = this.startsWithRegExp(input);
        return { contain, capturedText };
    }
}

const rule1 = new RawRule("hello");
const rule2 = new RegExpRule(" +");
const rule3 = new RawRule("world!");

const source = new Source("hello          world!");
source.addRule(rule1, rule2, rule3).parse();
console.log(source.getTokenList()); // ["hello", "          ", "world!"]
