interface Source {
    getContent(): string;
    setContent(s: string): void;
    getTokenList(): string[];
    appendToken(token: string): void;
    addRule(...rule: Rule[]): Source;
    parse(): void;
}

class SourceImpl implements Source {
    private readonly tokenList: string[] = [];
    private readonly rules: Rule[] = [];

    public constructor(private content: string) { }

    public getContent() {
        return this.content;
    }

    public setContent(s: string) {
        this.content = s
    }

    public getTokenList() {
        return this.tokenList;
    }

    public appendToken(token: string) {
        this.tokenList.push(token);
    }

    public addRule(...rule: Rule[]): Source {
        this.rules.push(...rule);
        return this;
    }

    public parse() {
        this.rules.forEach(rule => rule.visit(this));
    }
}

interface Rule {
    visit(source: Source): void;
}

class RawRule implements Rule {
    public constructor(private readonly rawText: string) {}

    public visit(source: Source) {
        const content = source.getContent();
        if (content.startsWith(this.rawText)) {
            source.setContent(content.replace(this.rawText, ''));
            source.appendToken(this.rawText);
        }
    }
}

class RegExpRule implements Rule {
    private readonly regExp: RegExp;
    public constructor(regText: string) { 
        this.regExp = new RegExp(regText);
    }

    private startsWithRegExp(source: Source) {
        const regExpExecArray = this.regExp.exec(source.getContent());
        const contain = regExpExecArray ? regExpExecArray.index === 0 : false;
        const capturedText = regExpExecArray ? regExpExecArray[0] : '';
        return { contain, capturedText };
    }

    public visit(source: Source) {
        const { contain, capturedText } = this.startsWithRegExp(source);
        if (contain) {
            const content = source.getContent();
            source.setContent(content.replace(capturedText, ''));
            source.appendToken(capturedText);
        }
    }
}

const rule1 = new RawRule("hello");
const rule2 = new RegExpRule(" +");
const rule3 = new RawRule("world!");

const source = new SourceImpl("hello          world!");
source.addRule(rule1, rule2, rule3).parse();
console.log(source.getTokenList()); // ["hello", "          ", "world!"]

