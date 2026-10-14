// src/lib/synonyms.ts

export const SYNONYMS: Record<string, string[]> = {
  "vitamin a":   ["retinyl acetate", "retinyl palmitate", "retinol", "vitamin a"],
  "vitamin e":   ["tocopherol", "tocopheryl acetate", "alpha-tocopherol", "vitamin e"],
  "vitamin b2":  ["riboflavin", "vitamin b2"],
  "riboflavin":  ["riboflavin", "vitamin b2"],
  "omega-3":     ["epa", "dha", "omega-3", "fish oil", "omacor", "pronova"],
  "lysine":      ["l-lysine", "lysine"],
  "citric acid": ["citric acid", "citrate"],
  "lactic acid": ["lactic acid", "lactate", "pla", "polylactic acid"],
  "pbat":        ["pbat", "ecoflex", "polybutylene adipate"],
  "phytase":     ["phytase", "natuphos"],
  "astaxanthin": ["astaxanthin", "haematococcus"],
  "beta-carotene": ["beta-carotene", "carotene", "lucaropen"],
  "msg":         ["monosodium glutamate", "msg", "glutamate"],
  "threonine":   ["l-threonine", "threonine"],
  "tryptophan":  ["l-tryptophan", "tryptophan"],
  "methionine":  ["dl-methionine", "methionine"],
  "basf":        ["basf"],
  "dsm-firmenich": ["dsm-firmenich", "dsm firmenich", "dsm", "firmenich"],
  "novonesis":   ["novonesis", "novozymes"],
  "iff":         ["iff", "international flavors"],
  "evonik":      ["evonik"],
  "adm":         ["adm", "archer daniels midland"],
  "cargill":     ["cargill"],
  "corbion":     ["corbion"],
}

const STOP_WORDS = new Set([
  "the","a","an","and","or","but","in","on","at","to","for","of","with",
  "by","from","is","are","was","were","be","been","have","has","do","does",
  "did","will","would","could","should","may","might","can","me","my","we",
  "our","you","your","they","their","what","where","when","how","who","which",
  "show","tell","find","list","give","each","produced","producing","makes",
  "made","manufacture","manufactured","produces","market","share","company",
  "companies","facility","facilities","plant","plants","site","sites",
])

export function expandTerms(query: string): string[] {
  const lower = query.toLowerCase()
  const terms = new Set<string>()

  // Add individual non-stop-word tokens from the query
  lower.split(/[\s,;.?!]+/).forEach((token) => {
    const clean = token.replace(/[^a-z0-9-]/g, "")
    if (clean.length > 1 && !STOP_WORDS.has(clean)) {
      terms.add(clean)
    }
  })

  // Expand known multi-word keys and their aliases
  for (const [key, aliases] of Object.entries(SYNONYMS)) {
    if (lower.includes(key)) {
      aliases.forEach((a) => terms.add(a))
    }
  }

  return [...terms]
}
