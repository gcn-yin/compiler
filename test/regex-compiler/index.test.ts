import compile, { isMatch } from "../../src/regex-compiler";

describe("test regex compiler", () => {
  it("basic cases", () => {
    expect(isMatch("a", "aa")).toEqual(false);
    expect(isMatch("aa", "a*")).toEqual(true);
    expect(isMatch("ab", ".*")).toEqual(true);
    expect(isMatch("aab", "c*a*b")).toEqual(true);
    expect(isMatch("mississippi", "mis*is*p*.")).toEqual(false);
  })

  it("without preprocess", () => {
    const matchResult = compile("a*a").match("aaa");
    expect(matchResult.match).toEqual(true);
  });
});
