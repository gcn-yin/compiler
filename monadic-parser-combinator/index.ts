type Parser<T> = (input: string) => Array<[T, string]>;

function bind<T, R>(p: Parser<T>, f: (t: T) => Parser<R>): Parser<R> {
  return (inp: string) => p(inp).map(it => f(it[0])(it[1]))
    .reduce((x, y) => x.concat(y), [])
}
