#!/usr/bin/env python3

# ISO/IEC 10646 & Unicode Standard Bidi Control Isolators
LRI = "\u2066"  # Left-to-Right Isolate
RLI = "\u2067"  # Right-to-Left Isolate
FSI = "\u2068"  # First Strong Isolate
PDI = "\u2069"  # Pop Directional Isolator

class BidiStreamParser:
    """Parses and balances bidirectional Unicode streams between system polarities."""
    
    @staticmethod
    def encapsulate_backend(data_str: str) -> str:
        return f"{LRI}{data_str}{PDI}"

    @staticmethod
    def encapsulate_frontend(data_str: str) -> str:
        return f"{RLI}{data_str}{PDI}"

    @staticmethod
    def parse_stream(bidi_payload: str) -> dict:
        lri_count = bidi_payload.count(LRI)
        rli_count = bidi_payload.count(RLI)
        pdi_count = bidi_payload.count(PDI)

        balanced = (lri_count + rli_count) == pdi_count
        
        clean_text = (
            bidi_payload.replace(LRI, "")
            .replace(RLI, "")
            .replace(FSI, "")
            .replace(PDI, "")
        )

        return {
            "balanced": balanced,
            "lri_backend_nodes": lri_count,
            "rli_frontend_nodes": rli_count,
            "pdi_terminations": pdi_count,
            "polarity_ratio": round(lri_count / rli_count, 4) if rli_count > 0 else 1.0,
            "extracted_payload": clean_text
        }
