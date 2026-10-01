"""C# language, types, OOP, LINQ and exceptions (32 cards)."""

TYPES = ["dotnet::csharp::types"]
OOP = ["dotnet::csharp::oop"]
LANG = ["dotnet::csharp::language"]
LINQ = ["dotnet::csharp::linq"]
EXC = ["dotnet::csharp::exceptions"]

CARDS = [
    dict(
        id="C01", tags=TYPES,
        q="What are the key differences between a class and a struct in C#?",
        a="A class is a reference type: lives on the heap, shared by reference, supports inheritance, can be null. A struct is a value type: copied on assignment, cannot inherit from another struct or class (only implement interfaces), cannot be null unless wrapped in `Nullable<T>`, and always has a zero-initialized default value. Struct `Equals` compares fields by default; class `Equals` compares references.",
        why="One of the most asked C# questions; it leads into copy bugs, boxing and when to use each.",
        ex="`struct Point { public int X, Y; }` — passing a `Point` to a method copies 8 bytes and the callee cannot affect the caller's copy; passing a class passes a reference and both sides see mutations.",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/struct",
    ),
    dict(
        id="C02", tags=TYPES,
        q="When should you choose a struct over a class?",
        a="Choose a struct when the type is small (about 16 bytes or less), logically represents a single value, is immutable, is short-lived or embedded in other objects, and will not be boxed frequently. Otherwise use a class.",
        why="Interviewers want the Microsoft guideline, not \"structs are faster\"; the wrong choice causes defensive copies and boxing.",
        ex="Good: `readonly record struct Money(decimal Amount, string Currency)`. Bad: a mutable 200-byte struct passed through many method calls.",
        src="https://learn.microsoft.com/dotnet/standard/design-guidelines/choosing-between-class-and-struct",
    ),
    dict(
        id="C03", tags=TYPES,
        q="What is a `record`, and how does it differ from a class?",
        a="A record is a reference type (or `record struct`) designed for immutable data. The compiler generates value-based `Equals`/`GetHashCode` and `==`, a readable `ToString`, deconstruction, and non-destructive mutation with `with`. Positional syntax declares init-only properties in one line.",
        why="Shows modern C# (9+) knowledge and understanding of value vs. reference equality.",
        ex="""```
public record Person(string Name, int Age);
var p1 = new Person("Ann", 30);
var p2 = p1 with { Age = 31 };
p1 == new Person("Ann", 30);   // true (value equality)
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record",
    ),
    dict(
        id="C04", tags=OOP,
        q="What is the difference between an interface and an abstract class?",
        a="An abstract class can hold state (fields), constructors and implemented members, and a class can inherit only one. An interface defines a contract, can be implemented many times, holds no instance state, and since C# 8 may carry default method implementations. Use an abstract class for an \"is-a\" base that shares code; use an interface for a \"can-do\" capability.",
        why="Perennial question; the follow-up is usually \"when would you pick one over the other\".",
        ex="`abstract class Shape { public abstract double Area(); public override string ToString() => $\"{GetType().Name}: {Area()}\"; }` vs `interface IShape { double Area(); }` — a `Circle` can be a `Shape` and also implement `IDrawable` and `IComparable<Shape>`.",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/abstract",
    ),
    dict(
        id="C05", tags=LANG,
        q="What is the difference between `const`, `readonly` and `static readonly`?",
        a="`const` is a compile-time constant (primitives, strings, null) baked into every calling assembly — change it and dependents must recompile. `readonly` is an instance field assignable only in the declaration or constructor, so each instance may differ. `static readonly` is assigned once at run time (static initializer or constructor) and can hold any type, including objects.",
        why="Checks you know the cross-assembly versioning trap of `const` and that `readonly` allows run-time values.",
        ex="""```
public const double Pi = 3.14159;                   // inlined at compile time
public static readonly HttpClient Client = new();   // runtime object, one per app
public readonly Guid Id = Guid.NewGuid();           // one per instance
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/readonly",
    ),
    dict(
        id="C06", tags=OOP,
        q="What does the `sealed` keyword do?",
        a="On a class, `sealed` prevents inheritance. On an overriding member, `sealed override` stops further overriding in derived classes. Sealing documents intent and lets the JIT devirtualize calls, giving a small performance gain.",
        why="Short, common question; shows you design for inheritance deliberately rather than by default.",
        ex="""```
public sealed class Config { }                    // class Derived : Config → compile error
public sealed override string ToString() => "x";  // subclasses cannot override again
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/sealed",
    ),
    dict(
        id="C07", tags=OOP,
        q="What is the difference between overriding a method (`virtual`/`override`) and hiding it (`new`)?",
        a="`override` replaces a `virtual` base method polymorphically: the derived version runs even through a base-typed reference. `new` hides the base method: which one runs depends on the compile-time type of the reference, so polymorphism is lost. Declaring a same-named method without either keyword hides it with a compiler warning.",
        why="A favourite trick question; demonstrates understanding of run-time vs. compile-time dispatch.",
        ex="""```
class A { public virtual string V() => "A"; public string H() => "A"; }
class B : A { public override string V() => "B"; public new string H() => "B"; }
A x = new B();
x.V();   // "B"  (override)
x.H();   // "A"  (hidden; static type is A)
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/new-modifier",
    ),
    dict(
        id="C08", tags=OOP,
        q="What are the C# access modifiers and what does each allow?",
        a="`public`: anywhere. `private`: the containing type only (default for members). `protected`: the containing type and derived types. `internal`: the same assembly (default for top-level types). `protected internal`: same assembly OR derived types. `private protected`: derived types within the same assembly only.",
        why="Quick-fire question; `protected internal` vs. `private protected` is the usual trap.",
        ex="`internal class Helper { }` is invisible to other projects unless the assembly declares `[assembly: InternalsVisibleTo(\"MyApp.Tests\")]`.",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers",
    ),
    dict(
        id="C09", tags=LANG,
        q="What is the difference between a field and a property, and what does the `init` accessor do?",
        a="A field is raw storage. A property is a pair of accessor methods (`get`/`set`) that can validate, compute, be virtual or appear in interfaces, while keeping field-like syntax; auto-properties generate the backing field. `init` (C# 9) allows assignment only during object construction or in an object initializer, enabling immutable objects without constructor boilerplate.",
        why="Explains why public fields are discouraged: no encapsulation, no data binding, and changing one later breaks binary compatibility.",
        ex="""```
public class User
{
    public string Email { get; init; } = "";    // settable only during initialization
    public bool IsActive { get; private set; }
}
var u = new User { Email = "a@b.com" };
u.Email = "x";   // compile error
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/init",
    ),
    dict(
        id="C10", tags=LANG,
        q="What is the difference between `ref`, `out` and `in` parameters?",
        a="All three pass by reference instead of copying. `ref` requires the argument to be initialized and lets the method read and modify it. `out` does not require initialization, but the method must assign it before returning. `in` passes a read-only reference, avoiding copies of large structs.",
        why="Tests understanding of the pass-by-value default and of the `TryParse` pattern.",
        ex="""```
bool ok = int.TryParse(text, out int value);          // out: assigned by the callee
void Swap(ref int a, ref int b) => (a, b) = (b, a);   // ref: both read and written
double Len(in Vector3 v) => Math.Sqrt(v.X * v.X + v.Y * v.Y + v.Z * v.Z);  // in: no copy
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/method-parameters",
    ),
    dict(
        id="C11", tags=LANG,
        q="What is a delegate, and what are `Func`, `Action` and `Predicate`?",
        a="A delegate is a type-safe reference to one or more methods with a given signature — a method pointer as an object. `Action<T...>` is the built-in delegate that returns void, `Func<T..., TResult>` returns a value, and `Predicate<T>` is equivalent to `Func<T, bool>`. Lambdas are the usual way to create them.",
        why="Delegates underpin events, LINQ, callbacks and async continuations.",
        ex="""```
Func<int, int, int> add = (a, b) => a + b;
Action<string> log = Console.WriteLine;
Predicate<int> isEven = n => n % 2 == 0;
add(2, 3);   // 5
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/delegates/",
    ),
    dict(
        id="C12", tags=LANG,
        q="What is an event, and how does it differ from exposing a public delegate field?",
        a="An event is a delegate with restricted access: outside code can only subscribe (`+=`) or unsubscribe (`-=`). With a public delegate field, any caller could invoke it or overwrite the whole invocation list with `=`. Convention: `EventHandler<TArgs>` with the `(object sender, TArgs e)` signature, raised with `?.Invoke` so a null (no subscribers) is safe.",
        why="Shows encapsulation of the observer pattern and awareness of the memory-leak risk of forgotten unsubscriptions.",
        ex="""```
public event EventHandler<OrderEventArgs>? OrderPlaced;
protected void OnOrderPlaced(Order o) => OrderPlaced?.Invoke(this, new OrderEventArgs(o));
// consumer:
service.OrderPlaced += (s, e) => Notify(e.Order);
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/events/",
    ),
    dict(
        id="C13", tags=LANG,
        q="What are extension methods, and how do you define one?",
        a="Extension methods are static methods in a static class whose first parameter is marked with `this`; the compiler lets you call them as if they were instance methods of that type. They add behavior to types you cannot modify (`string`, interfaces, third-party classes) without inheritance. LINQ is built entirely on them. They cannot access private members or override instance methods.",
        why="Explains how `.Where()` works on every `IEnumerable<T>`, and tests you know their limits.",
        ex="""```
public static class StringExtensions
{
    public static bool IsBlank(this string? s) => string.IsNullOrWhiteSpace(s);
}
"  ".IsBlank();   // true
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/extension-methods",
    ),
    dict(
        id="C14", tags=TYPES,
        q="Why use generics, and what do generic constraints (`where T : ...`) do?",
        a="Generics let you write type-safe, reusable code with a type parameter resolved at compile time: no casting, no boxing of value types (unlike `ArrayList`/`object`). Constraints restrict `T` so the method can use its members: `class`, `struct`, `new()`, `notnull`, `unmanaged`, a base class, or an interface.",
        why="Fundamental to collections, repositories and DI; constraints show you can design APIs beyond `List<T>`.",
        ex="""```
public T GetOrCreate<T>(string key) where T : class, new()
    => _cache.TryGetValue(key, out var v) ? (T)v : new T();
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters",
    ),
    dict(
        id="C15", tags=TYPES,
        q="What are covariance and contravariance in generics (`out T` / `in T`)?",
        a="Covariance (`out`) lets you use a more derived type where a base is expected: an `IEnumerable<string>` is usable as `IEnumerable<object>`, because `T` only flows out. Contravariance (`in`) lets you use a less derived type: an `Action<object>` is usable as `Action<string>`, because `T` only flows in. Invariant types like `List<T>` allow neither, which is why `List<string>` is not a `List<object>`.",
        why="Explains compile errors with collections of subtypes and the design of `IComparer<in T>` and `Func<out TResult>`.",
        ex="""```
IEnumerable<string> names = new List<string>();
IEnumerable<object> objs = names;          // OK: covariant
List<object> bad = new List<string>();     // compile error: invariant
Action<object> act = o => Console.WriteLine(o);
Action<string> strAct = act;               // OK: contravariant
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/concepts/covariance-contravariance/",
    ),
    dict(
        id="C16", tags=LANG,
        q="What do nullable reference types (C# 8) actually do, and how do `?.`, `??` and `!` relate?",
        a="With `<Nullable>enable</Nullable>`, the compiler treats `string` as non-nullable and `string?` as nullable and warns about possible null dereferences; it is purely static analysis — nothing changes at run time. `?.` short-circuits to null, `??` supplies a fallback, `??=` assigns when null, and `!` (null-forgiving) silences the warning without any check.",
        why="Interviewers test whether you know NRTs are compile-time annotations, not runtime guards, so you still validate inputs at API boundaries.",
        ex="""```
string? name = GetName();
int len = name?.Length ?? 0;        // 0 when null
string safe = name ?? "unknown";
name!.ToUpper();                    // warning suppressed; NRE if actually null
```""",
        src="https://learn.microsoft.com/dotnet/csharp/nullable-references",
    ),
    dict(
        id="C17", tags=TYPES,
        q="Why is `string` immutable, when should you use `StringBuilder`, and is `String` different from `string`?",
        a="Strings are immutable so they are thread-safe, can be interned and shared, and are safe as dictionary keys; every \"modification\" allocates a new string. Use `StringBuilder` when building a string in a loop or across many appends to avoid quadratic copying. `string` is simply the C# keyword alias for `System.String` — they are identical.",
        why="Classic question with a performance follow-up; also explains why comparing strings with `==` is safe.",
        ex="""```
var sb = new StringBuilder();
for (int i = 0; i < 10_000; i++) sb.Append(i).Append(',');
string csv = sb.ToString();   // one final allocation instead of 10,000 intermediate strings
```""",
        src="https://learn.microsoft.com/dotnet/standard/base-types/stringbuilder",
    ),
    dict(
        id="C18", tags=TYPES,
        q="What is the difference between `==`, `.Equals()` and `ReferenceEquals()`?",
        a="`ReferenceEquals` is always identity (same object). `==` is bound at compile time: for reference types it defaults to identity unless the operator is overloaded (`string` and records overload it to value equality). `Equals()` is a virtual method dispatched at run time: value types and records compare contents; classes default to identity unless overridden.",
        why="Common trap: two `object`-typed variables holding equal strings compare false with `==` but true with `Equals`.",
        ex="""```
string s1 = "abc", s2 = new string("abc".ToCharArray());
s1 == s2;                     // true  (string overloads ==)
(object)s1 == (object)s2;     // false (reference comparison)
s1.Equals(s2);                // true  (virtual, value comparison)
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/statements-expressions-operators/equality-comparisons",
    ),
    dict(
        id="C19", tags=TYPES,
        q="Why must you override `GetHashCode` when you override `Equals`?",
        a="Hash-based collections (`Dictionary`, `HashSet`) first pick a bucket by `GetHashCode` and only then call `Equals`. If two \"equal\" objects produce different hash codes they land in different buckets and lookups fail. The contract: equal objects must return equal hash codes (the reverse is not required). Use `HashCode.Combine(...)` over the same members `Equals` uses, and implement `IEquatable<T>` to avoid boxing.",
        why="Shows you understand the contract behind dictionaries and why records generate both for you.",
        ex="""```
public override bool Equals(object? o) => o is Money m && m.Amount == Amount && m.Currency == Currency;
public override int GetHashCode() => HashCode.Combine(Amount, Currency);
```""",
        src="https://learn.microsoft.com/dotnet/api/system.object.gethashcode",
    ),
    dict(
        id="C20", tags=LANG,
        q="What is the difference between the `is` and `as` operators and a direct cast?",
        a="A direct cast `(T)x` throws `InvalidCastException` on failure. `as` returns null instead of throwing, so it works only with reference or nullable types. `is` tests type compatibility and, with a pattern (`x is T t`), tests and assigns in one step — the idiomatic choice today.",
        why="Quick knowledge check plus a chance to show modern pattern-matching style.",
        ex="""```
if (shape is Circle c) Console.WriteLine(c.Radius);  // test + cast
var sq = shape as Square;      // null if not a Square
var tri = (Triangle)shape;     // throws if not a Triangle
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/operators/type-testing-and-cast",
    ),
    dict(
        id="C21", tags=LANG,
        q="What is the difference between `var` and `dynamic`?",
        a="`var` is compile-time type inference: the variable has one fixed static type, fully checked by the compiler, with zero runtime cost. `dynamic` defers all member binding to run time through the DLR, so typos compile but throw `RuntimeBinderException` when executed, and calls are much slower. Use `dynamic` for COM interop or truly dynamic data, never to avoid declaring types.",
        why="Candidates often confuse the two; knowing the runtime cost and when `dynamic` is justified matters.",
        ex="""```
var x = "hi";      x.Length;    // checked at compile time
dynamic d = "hi";  d.Lenght;    // compiles; throws RuntimeBinderException at run time
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/reference-types#the-dynamic-type",
    ),
    dict(
        id="C22", tags=LINQ,
        q="What is the difference between `IEnumerable<T>` and `IQueryable<T>`?",
        a="`IEnumerable<T>` represents in-memory iteration; LINQ operators on it run as compiled delegates in your process. `IQueryable<T>` extends it with an expression tree and a provider (such as EF Core) that translates the whole query into SQL executed by the database. Filtering an `IEnumerable` obtained from a DB loads all rows first; filtering an `IQueryable` pushes the `WHERE` to the server.",
        why="The number-one EF Core performance pitfall raised in interviews.",
        ex="""```
IQueryable<Order> q = db.Orders.Where(o => o.Total > 100);                  // SELECT ... WHERE Total > 100
IEnumerable<Order> e = db.Orders.AsEnumerable().Where(o => o.Total > 100);  // loads every row, filters in memory
```""",
        src="https://learn.microsoft.com/dotnet/api/system.linq.iqueryable-1",
    ),
    dict(
        id="C23", tags=LINQ,
        q="What does `yield return` do, and how does it relate to `IEnumerable`/`IEnumerator`?",
        a="`yield return` turns a method into an iterator: the compiler generates a state machine implementing `IEnumerable<T>`/`IEnumerator<T>` that produces one element each time `MoveNext()` is called, pausing between elements. Nothing runs until enumeration starts, so elements are produced lazily and infinite or huge sequences cost no memory up front. `foreach` calls `GetEnumerator()`, then `MoveNext()`/`Current` in a loop.",
        why="Shows understanding of lazy evaluation and how `foreach` works under the hood.",
        ex="""```
IEnumerable<int> Evens() { for (int i = 0; ; i += 2) yield return i; }
foreach (var n in Evens().Take(3)) Console.WriteLine(n);   // 0 2 4
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/statements/yield",
    ),
    dict(
        id="C24", tags=LINQ,
        q="What is deferred execution in LINQ, and which operators force immediate execution?",
        a="Most LINQ operators (`Where`, `Select`, `OrderBy`, `Skip`) build a query but do not run it; execution happens when the query is enumerated — in a `foreach` or by a materializing operator such as `ToList()`, `ToArray()`, `Count()`, `First()` or `Sum()`. Enumerating twice runs the query twice (two DB round-trips with EF Core), and the query observes data changes made before enumeration.",
        why="Explains double-query bugs, \"disposed DbContext\" errors, and why `ToList()` is placed deliberately.",
        ex="""```
var q = numbers.Where(n => n > 2);   // nothing executed yet
numbers.Add(10);
var list = q.ToList();               // runs now and includes 10
```""",
        src="https://learn.microsoft.com/dotnet/standard/linq/deferred-execution-lazy-evaluation",
    ),
    dict(
        id="C25", tags=LINQ,
        q="`IEnumerable<T>` vs `ICollection<T>` vs `IList<T>` vs `IReadOnlyList<T>`: which should a method accept or return?",
        a="`IEnumerable<T>` offers forward-only iteration; `ICollection<T>` adds `Count`, `Add`, `Remove`; `IList<T>` adds index access and insertion; `IReadOnlyList<T>` gives count and indexing without mutation. Accept the least specific type you need (usually `IEnumerable<T>`) and return the most useful non-mutable view (`IReadOnlyList<T>`) unless callers must modify it. Avoid returning a live `IQueryable`/deferred `IEnumerable` from data access unless that is the intent.",
        why="Tests API-design judgement: exposing `List<T>` leaks mutability; returning a deferred enumerable from a DB method hides when the query runs.",
        ex="""```
public IReadOnlyList<Order> GetOrders(IEnumerable<int> ids)
    => _db.Orders.Where(o => ids.Contains(o.Id)).ToList();
```""",
        src="https://learn.microsoft.com/dotnet/standard/design-guidelines/guidelines-for-collections",
    ),
    dict(
        id="C26", tags=EXC,
        q="What is the difference between `throw;` and `throw ex;` in a catch block?",
        a="`throw;` rethrows the current exception and preserves the original stack trace. `throw ex;` throws the same object again but resets its stack trace to the current line, destroying the information about where it originated. To add context, wrap it: `throw new MyException(\"...\", ex)` keeps the original in `InnerException`.",
        why="A very common code-review and interview catch.",
        ex="""```
catch (SqlException ex)
{
    _log.LogError(ex, "Query failed");
    throw;                                              // keeps the stack trace
    // or: throw new DataAccessException("Query failed", ex);
}
```""",
        src="https://learn.microsoft.com/dotnet/standard/exceptions/best-practices-for-exceptions",
    ),
    dict(
        id="C27", tags=EXC,
        q="When does a `finally` block run, and can a `return` in `try` and code in `finally` interfere?",
        a="`finally` runs after `try`/`catch` whether the block exits normally, by `return`/`break`, or by an exception (even one thrown inside a `catch`). It is skipped only if the process dies (`Environment.FailFast`, stack overflow, power loss). A `return` in `try` evaluates the return value before `finally` runs, so changing a local in `finally` does not change what is returned, and `return` inside `finally` is a compile error.",
        why="Common puzzle question; `finally` is also what `using` and `lock` compile into.",
        ex="""```
int F() { int x = 1; try { return x; } finally { x = 2; } }   // returns 1
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/statements/exception-handling-statements",
    ),
    dict(
        id="C28", tags=EXC,
        q="What are the best practices for defining and using custom exceptions?",
        a="Derive from `Exception` (not `ApplicationException`), end the name with `Exception`, provide the standard constructors (default, message, message + inner) and add properties for context such as `OrderId`. Throw only for exceptional conditions, never for control flow; catch the most specific type you can handle; never swallow exceptions silently; and reuse framework types (`ArgumentNullException`, `InvalidOperationException`) when they fit.",
        why="Shows familiarity with framework design guidelines and the cost of exceptions.",
        ex="""```
public class OrderNotFoundException : Exception
{
    public int OrderId { get; }
    public OrderNotFoundException(int id) : base($"Order {id} not found") => OrderId = id;
    public OrderNotFoundException(int id, Exception inner) : base($"Order {id} not found", inner) => OrderId = id;
}
```""",
        src="https://learn.microsoft.com/dotnet/standard/exceptions/how-to-create-user-defined-exceptions",
    ),
    dict(
        id="C29", tags=LANG,
        q="What is pattern matching in C#, and which patterns can a `switch` expression use?",
        a="Pattern matching tests a value against a shape and optionally extracts parts: type patterns (`is Circle c`), property patterns (`{ Status: Paid }`), positional patterns (`(0, 0)`), relational and logical patterns (`> 0 and < 10`, `not null`), and list patterns (`[first, .. rest]`). Switch expressions combine them concisely, and the compiler warns when the cases are not exhaustive.",
        why="Demonstrates modern C# (7–11) fluency; interviewers often ask you to rewrite an if/else chain.",
        ex="""```
decimal Shipping(Order o) => o switch
{
    { Total: >= 100 }               => 0,
    { Country: "US", Weight: < 2 }  => 5,
    null                            => throw new ArgumentNullException(nameof(o)),
    _                               => 15
};
```""",
        src="https://learn.microsoft.com/dotnet/csharp/fundamentals/functional/pattern-matching",
    ),
    dict(
        id="C30", tags=LANG,
        q="What is reflection, and what are attributes used for?",
        a="Reflection lets code inspect and invoke type metadata at run time: list properties, find methods, create instances (`Activator.CreateInstance`), read attributes. Attributes are declarative metadata attached to code (`[Obsolete]`, `[Required]`, `[HttpGet]`) that frameworks read through reflection. Reflection is slow compared with direct calls, so cache `MemberInfo` lookups or prefer source generators.",
        why="Explains how serializers, DI containers, test runners and ASP.NET routing work; interviewers ask about the cost.",
        ex="""```
var required = typeof(User).GetProperties()
    .Where(p => p.GetCustomAttribute<RequiredAttribute>() is not null);
var instance = Activator.CreateInstance(typeof(User));
```""",
        src="https://learn.microsoft.com/dotnet/csharp/advanced-topics/reflection-and-attributes/",
    ),
    dict(
        id="C31", tags=TYPES,
        q="What is the difference between a shallow copy and a deep copy?",
        a="A shallow copy (`MemberwiseClone`) creates a new object whose fields are copied as-is: value fields are duplicated, but reference fields still point to the same child objects. A deep copy recursively clones referenced objects so the two graphs share nothing. `ICloneable` does not specify which, so prefer an explicit copy method, a record with `with`, or serialization for deep copies.",
        why="Shared child objects cause \"changing A also changed B\" bugs.",
        ex="""```
public Order ShallowCopy() => (Order)MemberwiseClone();          // Lines list is shared
public Order DeepCopy() => new Order { Lines = Lines.Select(l => l with { }).ToList() };
```""",
        src="https://learn.microsoft.com/dotnet/api/system.object.memberwiseclone",
    ),
    dict(
        id="C32", tags=LINQ,
        q="What is the difference between `First`, `FirstOrDefault`, `Single` and `SingleOrDefault`?",
        a="`First` returns the first match and throws if there is none. `FirstOrDefault` returns `default` (null/0) when there is none. `Single` throws unless there is exactly one match (none or more than one both throw). `SingleOrDefault` returns `default` for none but still throws for more than one. Use `Single*` when more than one result would indicate a data bug, such as lookup by a unique key.",
        why="Quick-fire LINQ question; `Single` also makes EF Core fetch `TOP 2` to verify uniqueness.",
        ex="""```
db.Users.Single(u => u.Email == email);                                   // throws if duplicates exist
db.Users.FirstOrDefault(u => u.IsAdmin) ?? throw new NoAdminException();
```""",
        src="https://learn.microsoft.com/dotnet/api/system.linq.enumerable.single",
    ),
]
