interface Expr {
    match(s: string): { match: boolean, length: number };
}

class Seq implements Expr {
    constructor(public readonly expressions: Array<Expr>) { }

    match(s: string): { match: boolean, length: number } {
        let tmp = s;
        let length = 0;
        for (const exp of this.expressions) {
            const matchResult = exp.match(tmp);
            if (!matchResult.match) {
                return { match: false, length: 0 };
            }
            tmp = tmp.substr(0, length);
            length += matchResult.length;
        }
        return { match: true, length };
    }
}

class Char implements Expr {
    constructor(public readonly value: string) { }

    match(s: string): { match: boolean; length: number; } {
        const equals = this.value === s[0];
        return { match: equals, length: equals ? 1 : 0 };
    }
}

class AnyChar implements Expr {
    match(s: string): { match: boolean; length: number; } {
        return { match: true, length: 1 };
    }
}


function compile(s: string): Expr {
    const expressions = new Array<Expr>();
    for (let index = 0; index < s.length; index++) {
        const element = s[index];
        if (element >= 'a' || element <= 'z') {
            expressions.push(new Char(element));
        } else if (element === '.') {
            index++;
            const a = s[index];
            expressions.push(compile(a));
        } else if (element === '*') {
            expressions.push(new AnyChar());
        }
    }
    return new Seq(expressions);
}