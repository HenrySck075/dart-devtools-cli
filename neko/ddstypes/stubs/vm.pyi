
from __future__ import annotations
from typing_extensions import Generic
"Dart VM Core Object Types"
"the naming is literally java"
from typing import Any, Literal, TypeVar, TypedDict

class BoundField(TypedDict):
    decl: FieldReference
    name: str | int
    value: InstanceReference | Sentinel

class BoundVariable(Response):
    name: str
    value: InstanceReference | TypeArgumentsReference | Sentinel
    declarationTokenPos: int
    scopeStartTokenPos: int
    scopeEndTokenPos: int

class _BreakpointRequired(Object):
    location: SourceLocation
    breakpointNumber: int 
    enabled: bool 
    resolved: bool 

class Breakpoint(_BreakpointRequired,total=False):
    isSyntheticAsyncContinuation: bool

class _ClassReferenceRequired(ObjectReference):
    name: str 
    library: LibraryReference
class ClassReference(_ClassReferenceRequired,total=False):
    location: str
    typeParameters: list[str]

class _ClassRequired(ClassReference):
    abstract: bool
    const: bool
    isSealed: bool
    isMixinClass: bool
    isBaseClass: bool
    isInterfaceClass: bool
    isFinal: bool
    traceAllocations: bool
    interfaces: InstanceReference
    fields: FieldReference
    functions: FunctionReference
    subclasses: ClassReference
class Class(_ClassRequired,total=False):
    error: ErrorReference
    super: ClassReference
    superType: InstanceReference
    mixin: InstanceReference

class ClassHeapStats(TypedDict("ClassHeapStatsReserved",{"class": ClassReference}),Response):
    accumulatedSize: int
    bytesCurrent: int
    instancesAccumulated: int
    instancesCurrent: int

class CodeReference(ObjectReference):
    name: str
    kind: CodeKind
# @Object and Object are 2 different thing
class Code(Object):
    name: str
    kind: CodeKind

CodeKind = Literal[
    "Dart",
    "Native",
    "Stub",
    "Tag",
    "Collected"
]

class ContextReference(ObjectReference):
    length: int

class CpuSamplesEvent():
    samplePeriod: int
    maxStackDepth: int
    sampleCount: int
    timeOriginMicros: int
    timeExtentMicros: int
    pid: int
    samples: list[CpuSample]

class _CpuSampleRequired(TypedDict):
    tid: int
    timestamp: int
    stack: list[int]
class CpuSample(_CpuSampleRequired,total=False):
    vmTag: str
    userTag: str
    truncated: bool
    identityHashCode: int
    classId: int

class _ErrorRequired(Object):
    kind: ErrorKind
    message: str
ErrorReference = _ErrorRequired
class Error(_ErrorRequired,total=False):
    exception: InstanceReference
    stacktrace: InstanceReference

ErrorKind = Literal[
    "UnhandledException",
    "LanguageError",
    "InternalError",
    "TerminationError"
]

class _EventRequired(Response):
    kind: EventKind
    timestamp: int
class Event(_EventRequired,total=False):
    isolateGroup: IsolateGroupReference
    isolate: IsolateReference
    vm: VMReference
    breakpoint: Breakpoint
    pauseBreakpoints: list[Breakpoint]
    topFrame: Frame
    exception: InstanceReference
    bytes: str
    inspectee: InstanceReference
    gcType: str
    extensionRPC: str
    extensionKind: str
    extensionData: ExtensionData
    timelineEvents: list[TimelineEvent]
    updatedStreams: list[str]
    atAsyncSuspension: bool
    status: str
    logRecord: LogRecord
    service: str
    method: str
    alias: str
    flag: str
    newValue: str
    last: bool
    updatedTag: str
    previousTag: str
    cpuSamples: CpuSamplesEvent

EventKind = Literal[
    "VMUpdate",
    "VMFlagUpdate",
    "IsolateStart",
    "IsolateRunnable",
    "IsolateExit",
    "IsolateUpdate",
    "IsolateReload",
    "ServiceExtensionAdded",
    "PauseStart",
    "PauseExit",
    "PauseBreakpoint",
    "PauseInterrupted",
    "PauseException",
    "PausePostRequest",
    "Resume",
    "None",
    "BreakpointAdded",
    "BreakpointResolved",
    "BreakpointRemoved",
    "BreakpointUpdated",
    "GC",
    "WriteEvent",
    "Inspect",
    "Extension",
    "Logging",
    "TimelineEvents",
    "TimelineStreamSubscriptionsUpdate",
    "ServiceRegistered",
    "ServiceUnregistered",
    "UserTagChanged",
    "CpuSamples"
]

ExtensionData = dict[str, Any]

ExceptionPauseMode = int

class _FieldReferenceRequired(ObjectReference):
    name: str
    owner: ObjectReference
    declaredType: InstanceReference
    const: bool
    final: bool
    static: bool
class FieldReference(_FieldReferenceRequired,total=False):
    location: SourceLocation

class Field(FieldReference,total=False):
    staticValue: InstanceReference | Sentinel

class _FrameRequired(Response):
    index: int
class Frame(_FrameRequired,total=False):
    function: FunctionReference
    code: CodeReference
    location: SourceLocation
    vars: list[BoundVariable]
    kind: FrameKind

FrameKind = Literal[
    "Regular",
    "AsyncCausal",
    "AsyncSuspensionMarker"
]

class _FunctionReferenceRequired(ObjectReference):
    name: str
    static: bool
    const: bool
    implicit: bool
    abstract: bool
    isGetter: bool
    isSetter: bool
class FunctionReference(_FunctionReferenceRequired,total=False):
    location: SourceLocation

class _InstanceReferenceRequired(TypedDict("_InstanceReferenceRequiredReserved", {"class": ClassReference}),ObjectReference):
    kind: InstanceKind
    identityHashCode: int
class InstanceReference(_InstanceReferenceRequired,total=False):
    valueAsString: str
    valueAsStringIsTruncated: bool
    length: int
    name: str
    typeClass: ClassReference
    parameterizedClass: ClassReference
    returnType: InstanceReference
    parameters: list[Parameter]
    typeParameters: InstanceReference
    pattern: InstanceReference
    closureFunction: FunctionReference
    closureContext: ContextReference
    closureReceiver: InstanceReference
    portId: int
    allocationLocation: InstanceReference
    debugName: str
    label: str

class Instance(InstanceReference,total=False):
    offset: int
    count: int
    fields: list[BoundField]
    associations: list[MapAssociation]
    bytes: str
    mirrorReferent: ObjectReference
    isCaseSensitive: bool
    isMultiLine: bool
    propertyKey: ObjectReference
    propertyValue: ObjectReference
    target: ObjectReference
    typeArguments: TypeArgumentsReference
    parameterIndex: int
    targetType: InstanceReference
    bound: InstanceReference
    callback: InstanceReference
    callbackAddress: InstanceReference
    allEntries: InstanceReference
    value: InstanceReference
    token: InstanceReference
    detach: InstanceReference

InstanceKind = Literal[
    "PlainInstance",
    "Null",
    "Bool",
    "Double",
    "Int",
    "String",
    "List",
    "Map",
    "Set",
    "Record",
    "StackTrace",
    "Closure",
    "MirrorReference",
    "RegExp",
    "WeakProperty",
    "WeakReference",
    "Type",
    "TypeParameter",
    "TypeRef",
    "FunctionType",
    "RecordType",
    "BoundedType",
    "ReceivePort",
    "UserTag",
    "Finalizer",
    "NativeFinalizer",
    "FinalizerEntry"
]

class IsolateReference(Response):
    id: str 
    number: str 
    name: str 
    isSystemIsolate: bool 
    isolateGroupId: str 

class _IsolateRequired(IsolateReference):
    isolateFlags: list[IsolateFlag]
    startTime: int
    runnable: bool
    livePorts: int
    pauseOnExit: bool
    pauseEvent: Event
    libraries: LibraryReference
    breakpoints: list[Breakpoint]
    exceptionPauseMode: ExceptionPauseMode
class Isolate(_IsolateRequired,total=False):
    rootLib: LibraryReference
    error: Error
    extensionRPCs: list[str]

class IsolateFlag(TypedDict):
    name: str
    valueAsString: str

class IsolateGroupReference(Response):
    id: str
    number: str
    name: str
    isSystemIsolateGroup: bool
class IsolateGroup(IsolateGroupReference):
    isolates: list[IsolateReference]

class LibraryReference(ObjectReference):
    name: str
    uri: str

class LogRecord(Response):
    message: InstanceReference
    time: int
    level: int
    sequenceNumber: int
    loggerName: InstanceReference
    zone: InstanceReference
    error: InstanceReference
    stackTrace: InstanceReference

class MapAssociation(TypedDict):
    key: InstanceReference | Sentinel
    value: InstanceReference | Sentinel

class _MessageRequired(Response):
    index: int
    name: str
    messageObjectId: str
    size: int
class Message(_MessageRequired,total=False):
    handler: FunctionReference
    location: SourceLocation

class _ObjectReferenceRequired(Response):
    id: str 
class ObjectReference(_ObjectReferenceRequired,total=False):
    fixedId: str
class Object(ObjectReference,total=False):
    size:int 
#class Object(TypedDict("invalid",{"class": int}),_Object): pass

class _ParameterRequired(TypedDict):
    parameterType: InstanceReference
    fixed: bool
class Parameter(_ParameterRequired,total=False):
    name: str
    required: bool

class Response(TypedDict):
    type: str


class ScriptReference(ObjectReference):
    uri: str
class _ScriptRequired(Object):
    uri: str
    library: LibraryReference
class Script(_ScriptRequired,total=False):
    lineOffset: int
    columnOffset: int
    source: str
    tokenPosTable: list[list[int]]

class ScriptList(Response):
    scripts: list[ScriptReference]

class Sentinel(Response):
    kind: SentinelKind
    valueAsString: str

SentinelKind = Literal[
    "Collected",
    "Expired",
    "NotInitialized",
    "BeingInitialized",
    "OptimizedOut",
    "Free"
]

class _SourceLocationRequired(TypedDict):
    tokenPos: int 
    script: ScriptReference
class SourceLocation(_SourceLocationRequired, total=False):
    line: int 
    column: int 
    endTokenPos: int

class _StackRequired(Response):
    frames: list[Frame]
    messages: list[Message]
    truncated: bool
class Stack(_StackRequired,total=False):
    asyncCausalFrames: list[Frame]
    awaiterFrames: list[Frame]

#tleArgs = TypeVar("tleArgs", contravariant=True)
class TimelineEvent(TypedDict):
    name: str 
    "nam"
    cat: str 
    "category, meow"
    ph: str 
    "wtf"
    ts: int 
    pid: int 
    tid: int 
    args: dict

class TypeArgumentsReference(ObjectReference):
    name: str

class TypeArguments(TypeArgumentsReference):
    types: list[InstanceReference]

class VMReference(Response):
    name: str
class VM(VMReference):
    architectureBits: int
    hostCPU: str
    operatingSystem: str
    targetCPU: str
    version: str
    pid: int
    startTime: int
    isolates: list[IsolateReference]
    isolateGroups: list[IsolateGroupReference]
    systemIsolates: list[IsolateReference]
    systemIsolateGroups: list[IsolateGroupReference]



