# Pronunciation Normalization

Purpose

Normalize written words, names, terms, and expressions into forms that produce natural and accurate pronunciation in Text-to-Speech while preserving their original meaning and language.

---

## Core Rule

Do not change words merely because another pronunciation is possible.

Normalize pronunciation only when the written form is likely to be mispronounced, unnatural, ambiguous, or incorrectly interpreted by the TTS engine.

Prefer the natural pronunciation used by native speakers or the established pronunciation of the term.

---

## Native Language Preservation

Preserve words in their original language and script when the TTS system supports that language.

Examples

Bonjour
→ Bonjour

crème brûlée
→ crème brûlée

déjà vu
→ déjà vu

नमस्ते
→ नमस्ते

こんにちは
→ こんにちは

Do not automatically transliterate or translate foreign words.

---

## Code-Switching

When a sentence contains a word or phrase from another language, preserve the foreign-language word if it is naturally used in that form.

Example

The French phrase "au revoir" means "goodbye."

Do not replace it with an English phonetic spelling unless the TTS engine cannot pronounce the original correctly.

---

## Grapheme-to-Phoneme Normalization

Convert written forms into pronunciation-friendly forms only when the TTS engine is likely to pronounce the original incorrectly.

Examples

GIF
→ gif

GIF
→ jiff, if the intended pronunciation is the soft-G pronunciation

SQL
→ sequel, when referring to the database language and that is the intended pronunciation

SQL
→ S Q L, when the letters are intended to be pronounced individually

---

## Acronym and Initialism Pronunciation

Follow the established spoken pronunciation of the term.

Examples

AI
→ A I

GPU
→ G P U

NASA
→ NASA

NATO
→ NATO

Do not expand terms into their full meanings merely to make pronunciation easier.

AI
→ A I

Not:

AI
→ artificial intelligence

unless the original context specifically requires the expanded phrase.

---

## Proper Names

Preserve the original spelling of names unless the TTS engine consistently mispronounces the name.

Do not invent pronunciations.

Use documented or established pronunciations when available.

Examples

Mikhail Gorbachev
→ preserve the original name unless pronunciation normalization is required

---

## Foreign Names

Preserve the original spelling and language where possible.

Do not replace a foreign name with an English approximation unless necessary for accurate TTS pronunciation.

---

## Homographs

Use context to resolve words with multiple pronunciations.

Examples

lead
→ lead, when referring to the metal

lead
→ lead, when referring to guiding someone

read
→ read, present tense

read
→ read, past tense

Do not alter the written word unless the TTS engine requires a pronunciation-specific normalization.

---

## Ambiguous Pronunciation

If a written form can be pronounced in multiple common ways, use the context to determine the intended pronunciation.

Do not guess when context is insufficient.

---

## Brand and Product Names

Use the established pronunciation of the brand or product.

Follow dedicated product and brand knowledge documents when available.

Examples

NVIDIA
→ use the established pronunciation

RTX 4090
→ follow product-specific model pronunciation rules

Do not apply generic number or abbreviation rules to product names when a dedicated rule exists.

---

## Symbols and Special Characters

Replace symbols with spoken equivalents only when required for natural pronunciation.

Examples

&
→ and

%
→ percent

@
→ at

Do not replace symbols when they are part of an official name, product name, username, or other entity whose original form should be preserved.

---

## Pronunciation Overrides

When a term is consistently mispronounced by the TTS engine, use a pronunciation-friendly written form only if it preserves the intended pronunciation and meaning.

Example

Written form:
SQL

Pronunciation target:
sequel

Normalization:
sequel

---

## Rule Priority

1. Preserve the original meaning.
2. Preserve the original language.
3. Preserve the original word or name whenever pronunciation is already correct.
4. Use established native or domain pronunciation.
5. Use context to resolve ambiguity.
6. Apply pronunciation normalization only when it improves TTS output.
7. Follow more specific knowledge documents when available.

---

## Never

- Never invent pronunciations.
- Never transliterate foreign words unnecessarily.
- Never translate foreign words merely for pronunciation.
- Never expand abbreviations automatically.
- Never replace natural spoken forms with formal dictionary expansions.
- Never change a word solely because a different pronunciation is possible.
- Never alter proper names without a pronunciation reason.
- Never apply generic rules when a more specific knowledge document exists.
- Never change the meaning of the original text.
