"""CLR, memory and runtime fundamentals (12 cards)."""

T = ["dotnet::runtime"]

CARDS = [
    dict(
        id="R01", tags=T,
        q="What is the CLR (Common Language Runtime) and what does it do?",
        a="The CLR is .NET's execution engine (virtual machine). It loads assemblies, JIT-compiles IL to native code, manages memory with the garbage collector, enforces type safety, and handles exceptions, threading and security.",
        why="Almost every .NET interview starts here; it frames what \"managed code\" means and why GC, JIT and IL exist.",
        ex="`dotnet run` → the C# compiler emits IL into MyApp.dll → the CLR loads it, JIT-compiles `Main` and each method on first call, and collects garbage while it runs.",
        src="https://learn.microsoft.com/dotnet/standard/clr",
    ),
    dict(
        id="R02", tags=T,
        q="What is IL (CIL / MSIL), and why does C# compile to it instead of native code?",
        a="IL is a CPU-independent intermediate language stored in assemblies. Compiling to IL lets every .NET language (C#, F#, VB) share one runtime and library ecosystem, and lets the JIT optimize for the actual CPU and OS at run time.",
        why="Explains language interoperability and why one DLL runs unchanged on Windows, Linux and macOS.",
        ex="`ildasm MyApp.dll` (or ILSpy) shows IL such as `ldarg.0`, `call`, `ret` instead of x64 instructions.",
        src="https://learn.microsoft.com/dotnet/standard/managed-execution-process",
    ),
    dict(
        id="R03", tags=T,
        q="What is the difference between managed and unmanaged code?",
        a="Managed code runs under the CLR, which handles memory, type safety and exceptions for it. Unmanaged code (C/C++, Win32 APIs, COM) runs outside the CLR and manages its own memory; you call it through P/Invoke or COM interop and must release its resources yourself.",
        why="Shows you understand where GC safety ends and why `IDisposable` and `SafeHandle` exist for native resources.",
        ex="""```
[DllImport("user32.dll", CharSet = CharSet.Unicode)]
static extern int MessageBox(IntPtr hWnd, string text, string caption, uint type);
```
calls unmanaged Win32 code from C#.""",
        src="https://learn.microsoft.com/dotnet/standard/managed-code",
    ),
    dict(
        id="R04", tags=T,
        q="What is JIT compilation in .NET, and how do tiered compilation and AOT change it?",
        a="The JIT compiles each method from IL to native code the first time it is called, then caches it. Tiered compilation first emits quick, lightly optimized code (tier 0) and recompiles hot methods with full optimizations (tier 1). ReadyToRun and Native AOT precompile ahead of time to cut startup time and memory, trading some runtime optimizations and reflection flexibility.",
        why="Explains startup vs. steady-state performance trade-offs and when to pick Native AOT (serverless, CLI tools, containers).",
        ex="`<PublishAot>true</PublishAot>` in the .csproj produces a self-contained native executable with no JIT at run time.",
        src="https://learn.microsoft.com/dotnet/core/runtime-config/compilation",
    ),
    dict(
        id="R05", tags=T,
        q="What is the difference between .NET Framework, .NET Core and .NET 5+ (and where does .NET Standard fit)?",
        a=".NET Framework (4.8) is Windows-only, ships with Windows and is in maintenance mode. .NET Core was its cross-platform, open-source rewrite. From .NET 5 the two lines merged into a single \"modern .NET\" (even versions such as 8 and 10 are LTS), which is where all new features go. .NET Standard was a spec for libraries targeting both worlds; new libraries should target modern .NET and use `netstandard2.0` only when legacy consumers need them.",
        why="Interviewers check you know which runtime is current, what LTS means, and how to plan a migration.",
        ex="A `net8.0` class library cannot be referenced by a .NET Framework 4.8 app; multi-target `net8.0;netstandard2.0` to share code with it.",
        src="https://learn.microsoft.com/dotnet/standard/net-standard",
    ),
    dict(
        id="R06", tags=T,
        q="What is an assembly in .NET?",
        a="An assembly (.dll or .exe) is the unit of deployment, versioning and security. It contains IL code, metadata describing every type, and a manifest with the assembly's name, version, culture, public key and referenced assemblies.",
        why="Underpins NuGet packaging, version conflicts, `InternalsVisibleTo`, and reflection-based loading.",
        ex="`typeof(string).Assembly.FullName` → `System.Private.CoreLib, Version=8.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e`",
        src="https://learn.microsoft.com/dotnet/standard/assembly/",
    ),
    dict(
        id="R07", tags=T,
        q="How does the .NET garbage collector decide what to free, and how does it reclaim memory?",
        a="It is a tracing, generational, compacting collector. Starting from roots (stack variables, static fields, CPU registers, GC handles) it marks every reachable object; everything unmarked is garbage. It then compacts the survivors so free memory stays contiguous and allocation remains a cheap pointer bump.",
        why="Explains why *unreachable* objects (not \"unused\" ones) get collected, and why allocation is fast but collections cause pauses.",
        ex="`var list = new List<int>(); list = null;` — the list becomes unreachable and is reclaimed at the next gen-0 collection, not immediately.",
        src="https://learn.microsoft.com/dotnet/standard/garbage-collection/fundamentals",
    ),
    dict(
        id="R08", tags=T,
        q="What are GC generations 0, 1 and 2, and what is the Large Object Heap (LOH)?",
        a="Gen 0 holds new objects and is collected often and cheaply; survivors are promoted to gen 1, then to gen 2 (long-lived objects, collected rarely). This works because most objects die young. Objects of 85,000 bytes or more go straight to the Large Object Heap, which is collected together with gen 2 and is not compacted by default.",
        why="Explains why many short-lived allocations are cheap but large arrays and long-lived caches are expensive, and why LOH churn causes fragmentation.",
        ex="`new byte[100_000]` lands on the LOH; allocating one per request triggers frequent, expensive gen-2 collections — rent from `ArrayPool<byte>.Shared` instead.",
        src="https://learn.microsoft.com/dotnet/standard/garbage-collection/large-object-heap",
    ),
    dict(
        id="R09", tags=T,
        q="What is the difference between `IDisposable.Dispose()` and a finalizer (`~ClassName`)?",
        a="`Dispose()` is called deterministically by your code (usually via `using`) to release unmanaged or scarce resources right away. A finalizer runs non-deterministically on the finalizer thread when the GC collects the object, and only as a safety net. Prefer `Dispose`; add a finalizer only when you directly own an unmanaged handle — and even then, wrap it in `SafeHandle` instead.",
        why="Classic question; tests whether you know the GC does not manage files, sockets or DB connections for you.",
        ex="""```
public void Dispose()
{
    Dispose(disposing: true);
    GC.SuppressFinalize(this); // already cleaned up, skip the finalizer
}
```""",
        src="https://learn.microsoft.com/dotnet/standard/garbage-collection/implementing-dispose",
    ),
    dict(
        id="R10", tags=T,
        q="What does the `using` statement do, and what is a using declaration?",
        a="`using (var x = ...) { }` guarantees `x.Dispose()` runs when the block exits — normally or by exception — because it compiles to try/finally. A using declaration (C# 8) `using var x = ...;` does the same but disposes at the end of the enclosing scope, avoiding nested blocks.",
        why="Shows you know how to avoid leaking connections, streams and HTTP responses.",
        ex="""```
using var conn = new SqlConnection(cs);
await conn.OpenAsync();
// conn.Dispose() runs automatically when the method returns
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/statements/using",
    ),
    dict(
        id="R11", tags=T,
        q="What is the difference between value types and reference types in C#?",
        a="Value types (`struct`, `enum`, primitives) hold their data directly and are copied on assignment. Reference types (`class`, `interface`, `delegate`, `string`, arrays) hold a reference to an object on the managed heap, so assignment copies the reference and both variables see the same object. Where a value lives depends on its container: a local struct is on the stack, but a struct field inside a class lives on the heap with its owner.",
        why="Explains copy semantics, nullability, default equality and boxing — and catches the \"value types are always on the stack\" myth.",
        ex="""```
var a = new Point(1, 2); var b = a; b.X = 9;        // a.X is still 1 (struct copied)
var c = new Person();    var d = c; d.Name = "X";   // c.Name is "X" (same object)
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/value-types",
    ),
    dict(
        id="R12", tags=T,
        q="What are boxing and unboxing, and why do they matter for performance?",
        a="Boxing wraps a value type in a heap-allocated `object` (or interface reference) so it can be treated as a reference; unboxing copies it back out with an explicit cast. Every box is an allocation plus GC pressure, and unboxing to the wrong type throws `InvalidCastException`.",
        why="A common hidden cost in hot paths: non-generic collections, `string.Format` with ints, calling interface methods on structs.",
        ex="""```
int n = 42;
object o = n;      // boxing: allocates
int m = (int)o;    // unboxing
long l = (long)o;  // InvalidCastException (must unbox to the exact type)
```""",
        src="https://learn.microsoft.com/dotnet/csharp/programming-guide/types/boxing-and-unboxing",
    ),
]
