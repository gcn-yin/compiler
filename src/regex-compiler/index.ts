/**
 * From leetcode
 * Given an input string (s) and a pattern (p), implement regular expression matching with support for '.' and '*'.
 *
 * '.' Matches any single character.
 * '*' Matches zero or more of the preceding element.
 * The matching should cover the entire input string (not partial).
 *
 * Note:
 *
 * s could be empty and contains only lowercase letters a-z.
 * p could be empty and contains only lowercase letters a-z, and characters like . or *.
 * Example 1:
 *
 * Input:
 * s = "aa"
 * p = "a"
 * Output: false
 * Explanation: "a" does not match the entire string "aa".
 * Example 2:
 *
 * Input:
 * s = "aa"
 * p = "a*"
 * Output: true
 * Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
 * Example 3:
 *
 * Input:
 * s = "ab"
 * p = ".*"
 * Output: true
 * Explanation: ".*" means "zero or more (*) of any character (.)".
 * Example 4:
 *
 * Input:
 * s = "aab"
 * p = "c*a*b"
 * Output: true
 * Explanation: c can be repeated 0 times, a can be repeated 1 time. Therefore, it matches "aab".
 * Example 5:
 *
 * Input:
 * s = "mississippi"
 * p = "mis*is*p*."
 * Output: false
 */

interface Expr {
  match(s: string): { match: boolean; length: number };
}

class Sequence implements Expr {
  constructor(public readonly expressions: Array<Expr>) {}

  match(s: string): { match: boolean; length: number } {
    let tmp = s;
    let length = 0;
    for (const exp of this.expressions) {
      const matchResult = exp.match(tmp);
      if (!matchResult.match) {
        return { match: false, length: 0 };
      }
      tmp = tmp.substring(matchResult.length, tmp.length);
      length += matchResult.length;
    }
    return { match: true, length };
  }
}

class SingleChar implements Expr {
  constructor(private readonly value: string) {}

  match(s: string): { match: boolean; length: number } {
    const equals = this.value === s[0];
    return { match: equals, length: equals ? 1 : 0 };
  }
}

class AnyChar implements Expr {
  match(s: string): { match: boolean; length: number } {
    if (s.length === 0) {
      return { match: false, length: 1 };
    }
    return { match: true, length: 1 };
  }
}

class ZeroOrMore implements Expr {
  constructor(private readonly expr: Expr | null) {}

  match(s: string): { match: boolean; length: number } {
    let tmp = s;
    let result = 0;
    // eslint-disable-next-line no-constant-condition
    while (true) {
      const { match, length } = this.expr?.match(tmp) || { match: false, length: 0 };
      if (!match) {
        break;
      }
      tmp = tmp.substring(length, tmp.length);
      result += length;
    }
    return { match: true, length: result };
  }
}

function compile(s: string): Expr {
  const expressions = new Array<Expr>();
  for (let index = 0; index < s.length; index++) {
    const element = s[index];
    if (element >= "a" && element <= "z") {
      expressions.push(new SingleChar(element));
    } else if (element === "*") {
      expressions.push(new ZeroOrMore(expressions.pop() || null));
    } else if (element === ".") {
      expressions.push(new AnyChar());
    }
  }
  return new Sequence(expressions);
}

export function isMatch(s: string, p: string): boolean {
  const matchResult = compile(p).match(s);
  return matchResult.length === s.length;
}

// function preProcess(s: string): string {
//     const array = new Array<string>();
//     let tmp = s;
//     while (true) {
//         const starIndex = tmp.indexOf("*");
//         if (starIndex < 0) {
//             array.push(tmp);
//             break;
//         }
//         if (starIndex == tmp.length - 1) {
//             array.push(tmp);
//             break;
//         }
//         if (tmp.charAt(starIndex - 1) == tmp.charAt(starIndex + 1)) {
//             array.push(tmp.charAt(starIndex - 1) )
//         }
//     }
//     return array.join("");
// }

export default compile;
