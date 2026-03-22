/**
 * PEP — Protocol for Evolutionary Programs
 * TypeScript type definitions for all 7 specifications.
 */

// ── Branded types ──────────────────────────────────────────────────────────────

declare const __uuid: unique symbol;
declare const __semver: unique symbol;

/** UUID v4 string branded type. */
export type UUID = string & { readonly [__uuid]: never };

/** Semantic version string branded type. */
export type SemVer = string & { readonly [__semver]: never };

/** ISO 8601 datetime string. */
export type ISODateTime = string;

// ── PEP-001 Organism ──────────────────────────────────────────────────────────

export type OrganismStatus = "embryo" | "alive" | "dormant" | "dead";

export interface Trait {
  name: string;
  value: unknown;
  weight: number;
}

export interface OrganismMutation {
  gene: string;
  operation: "add" | "remove" | "modify";
  payload: unknown;
}

export interface Genome {
  traits: Trait[];
  mutations: OrganismMutation[];
}

export interface Constraint {
  resource: string;
  limit: number;
}

export interface Phenotype {
  capabilities: string[];
  constraints: Constraint[];
}

export interface OrganismMetadata {
  created_at: ISODateTime;
  updated_at: ISODateTime;
  tags: string[];
  lineage: UUID[];
}

export interface Organism {
  id: UUID;
  name: string;
  version: SemVer;
  genome: Genome;
  phenotype: Phenotype;
  metadata: OrganismMetadata;
  status: OrganismStatus;
}

// ── PEP-002 Judge ─────────────────────────────────────────────────────────────

export type JudgeMetric = "accuracy" | "latency" | "cost" | "safety" | "creativity";

export interface Criterion {
  name: string;
  weight: number;
  threshold: number;
  metric: JudgeMetric;
}

export interface VerdictDetail {
  criterion: string;
  score: number;
  passed: boolean;
}

export interface Verdict {
  organism_id: UUID;
  score: number;
  passed: boolean;
  details: VerdictDetail[];
}

export interface JudgeConfig {
  max_retries: number;
  timeout_ms: number;
  parallel: boolean;
}

export interface Judge {
  id: UUID;
  name: string;
  version: SemVer;
  criteria: Criterion[];
  verdict: Verdict;
  config: JudgeConfig;
}

// ── PEP-003 Engine ────────────────────────────────────────────────────────────

export type SelectionStrategy = "tournament" | "roulette" | "rank" | "elite";
export type CrossoverMethod = "single_point" | "two_point" | "uniform" | "none";

export interface Population {
  size: number;
  organisms: UUID[];
  generation: number;
}

export interface Selection {
  strategy: SelectionStrategy;
  pressure: number;
  elitism_rate: number;
}

export interface CrossoverConfig {
  method: CrossoverMethod;
  rate: number;
}

export interface MutationConfig {
  rate: number;
  decay: number;
}

export interface Termination {
  max_generations: number;
  fitness_target: number;
  stagnation_limit: number;
}

export interface Engine {
  id: UUID;
  name: string;
  version: SemVer;
  population: Population;
  selection: Selection;
  crossover: CrossoverConfig;
  mutation: MutationConfig;
  termination: Termination;
}

// ── PEP-004 Event Log ─────────────────────────────────────────────────────────

export type EventLogType =
  | "organism.created"
  | "organism.mutated"
  | "organism.evaluated"
  | "organism.died"
  | "generation.started"
  | "generation.completed"
  | "engine.started"
  | "engine.stopped"
  | "judge.verdict"
  | "sharing.exported"
  | "sharing.imported"
  | "privacy.redacted"
  | "agent.action";

export type SourceComponent = "organism" | "judge" | "engine" | "sharing" | "privacy" | "agent";

export interface EventSource {
  component: SourceComponent;
  id: UUID;
}

export interface EventLog {
  id: UUID;
  timestamp: ISODateTime;
  type: EventLogType;
  source: EventSource;
  payload: Record<string, unknown>;
  sequence: number;
  correlation_id?: UUID;
  checksum: string;
}

// ── PEP-005 Sharing ───────────────────────────────────────────────────────────

export type SharingFormat = "pep-native" | "onnx" | "safetensors" | "json" | "custom";
export type TargetProtocol = "https" | "ipfs" | "s3" | "local";
export type IntegrityAlgorithm = "sha256" | "sha512" | "blake3";

export interface SharingSource {
  organism_id: UUID;
  engine_id: UUID;
  generation: number;
}

export interface SharingTarget {
  uri: string;
  protocol: TargetProtocol;
}

export interface SharingContent {
  genome: boolean;
  phenotype: boolean;
  history: boolean;
  size_bytes: number;
}

export interface IntegrityInfo {
  algorithm: IntegrityAlgorithm;
  hash: string;
  signature?: string;
}

export interface SharingPermissions {
  public: boolean;
  allowed_consumers: UUID[];
  expires_at?: ISODateTime;
}

export interface SharingManifest {
  id: UUID;
  format: SharingFormat;
  source: SharingSource;
  target: SharingTarget;
  content: SharingContent;
  integrity: IntegrityInfo;
  permissions: SharingPermissions;
}

// ── PEP-006 Privacy ───────────────────────────────────────────────────────────

export type PrivacyScope = "organism" | "judge" | "engine" | "event" | "global";
export type RuleAction = "redact" | "hash" | "encrypt" | "omit" | "generalize";
export type ConditionContext = "export" | "log" | "api" | "always";

export interface RuleCondition {
  context: ConditionContext;
}

export interface PrivacyRule {
  field: string;
  action: RuleAction;
  condition?: RuleCondition;
}

export interface Retention {
  max_age_days: number;
  auto_purge: boolean;
  archive_after_days?: number;
}

export interface Consent {
  required: boolean;
  granted_by?: UUID;
  granted_at?: ISODateTime;
}

export interface AuditConfig {
  log_access: boolean;
  log_mutations: boolean;
  require_justification: boolean;
}

export interface PrivacyPolicy {
  id: UUID;
  version: SemVer;
  scope: PrivacyScope;
  rules: PrivacyRule[];
  retention: Retention;
  consent: Consent;
  audit: AuditConfig;
}

// ── PEP-007 Agent ─────────────────────────────────────────────────────────────

export type AgentRole = "evolver" | "guardian" | "explorer" | "harvester" | "orchestrator";
export type AgentStatusValue = "idle" | "active" | "suspended" | "terminated";

export interface AgentBindings {
  engine_id?: UUID;
  organism_ids: UUID[];
  judge_ids: UUID[];
}

export interface AgentPolicy {
  max_actions_per_minute: number;
  require_approval: boolean;
  allowed_actions: string[];
  denied_actions: string[];
}

export interface AgentState {
  status: AgentStatusValue;
  current_task?: string;
  last_action_at?: ISODateTime;
  error_count: number;
}

export interface Agent {
  id: UUID;
  name: string;
  version: SemVer;
  role: AgentRole;
  capabilities: string[];
  bindings: AgentBindings;
  policy: AgentPolicy;
  state: AgentState;
}
