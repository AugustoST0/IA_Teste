import numpy as np

# =====================================================================
# 1. FRAMEWORK DE IA: MODELO BAYESIANO DE PREDIÇÃO
# =====================================================================
def modelo_bayesiano_risco_clima(temperatura: float, umidade: float) -> float:
    """
    Simula o motor probabilístico da Defesa Civil para cálculo de risco de desastres.
    """
    fator_termico = temperatura / 40.0
    fator_umidade = umidade / 100.0

    if umidade <= 85.0:
        probabilidade = (fator_termico * 0.4 + fator_umidade * 0.6) * 100
        return min(max(probabilidade, 0.0), 100.0)
    else:
        probabilidade = (fator_termico * 0.4 + (fator_umidade * 1.2)) * 100
        return min(max(probabilidade, 0.0), 100.0)


# =====================================================================
# 2. MOTOR DE ENGENHARIA DE QUALIDADE (QA & SRE)
# =====================================================================
class GuardiaoQualidadeIA:
    def __init__(self):
        self.limite_superior_temp = 38.0
        self.limite_inferior_umidade = 20.0

    def verificar_data_drift(self, lote_temperaturas: list, lote_umidades: list) -> bool:
        """Avalia a consistência estocástica dos dados de produção."""
        media_temp = float(np.mean(lote_temperaturas))
        media_umi = float(np.mean(lote_umidades))

        desvio_temp = float(np.std(lote_temperaturas))
        desvio_umi = float(np.std(lote_umidades))

        print(f"-> Analisando Lote - Média Temp: {media_temp:.1f}°C (DP: {desvio_temp:.1f}°C) | Média Umidade: {media_umi:.1f}% (DP: {desvio_umi:.1f}%)")

        if desvio_temp > 5.0 or desvio_umi > 15.0:
            print("🚨 [ALERTA CRÍTICO] Alta volatilidade detectada nos sensores!")
            return False

        if media_temp > self.limite_superior_temp or media_umi < self.limite_inferior_umidade:
            print("❌ [ALERTA DE QUALIDADE] Data Drift Detectado! Clima fora do padrão.")
            return False

        print("✅ [SUCESSO] Dados aprovados no teste de consistência.")
        return True

    def testar_relacao_metamorfica_umidade(self, temp_fixa: float, umidade_base: float) -> bool:
        """Valida a propriedade de monotonicidade do modelo em relação à umidade."""
        umidade_elevada = umidade_base + 15.0
        
        risco_base = modelo_bayesiano_risco_clima(temp_fixa, umidade_base)
        risco_alto = modelo_bayesiano_risco_clima(temp_fixa, umidade_elevada)
        
        print(f"\n[Teste Metamórfico] Mantendo {temp_fixa}°C fixos:")
        print(f"   * Cenário A (Umidade {umidade_base:.1f}%): Risco de Desastre = {risco_base:.1f}%")
        print(f"   * Cenário B (Umidade {umidade_elevada:.1f}%): Risco de Desastre = {risco_alto:.1f}%")
        
        if risco_alto >= risco_base:
            print("✅ [SUCESSO] Propriedade Metamórfica Mantida. IA agindo de forma lógica.")
            return True
        else:
            print("❌ [BUG CRÍTICO DETECTADO] O ar saturou de umidade, mas o risco calculado CAIU! A IA alucinou.")
            return False
    
    def testar_relacao_metamorfica_temperatura(self, umidade_fixa: float, temp_base: float) -> bool:
        """Valida que o aumento de temperatura aumenta ou mantém estável o risco calculado."""
        temp_elevada = temp_base + 5.0

        risco_base = modelo_bayesiano_risco_clima(temp_base, umidade_fixa)
        risco_alto = modelo_bayesiano_risco_clima(temp_elevada, umidade_fixa)

        print(f"\n[Teste Metamórfico Temperatura] Mantendo {umidade_fixa:.1f}% de umidade fixa:")
        print(f"   * Cenário Inicial (Temp {temp_base:.1f}°C): Risco de Desastre = {risco_base:.1f}%")
        print(f"   * Cenário Elevado (Temp {temp_elevada:.1f}°C): Risco de Desastre = {risco_alto:.1f}%")

        if risco_alto >= risco_base:
            print("✅ [SUCESSO] Propriedade Metamórfica de Temperatura Mantida.")
            return True
        else:
            print("❌ [BUG CRÍTICO DETECTADO] A temperatura subiu, mas o risco calculado diminuiu!")
            return False


# =====================================================================
# 3. EXECUÇÃO DOS CENÁRIOS DE TESTE
# =====================================================================
if __name__ == "__main__":
    guardiao = GuardiaoQualidadeIA()
    
    print("=== FASE 1: TESTES DE DATA DRIFT (ENTRADA DE DADOS) ===")
    
    print("\n--- Testando Lote 1 (Sensores Normais) ---")
    guardiao.verificar_data_drift([22.5, 24.0, 23.1, 25.8], [70.0, 75.5, 72.0, 68.0])
    
    print("\n--- Testando Lote 2 (Anomalia Térmica Extrema / Mudança Climática) ---")
    guardiao.verificar_data_drift([42.0, 44.5, 41.2, 43.0], [15.0, 12.5, 18.0, 14.2])
    
    print("\n--- Testando Lote 3 (Sensores Instáveis / Camuflados pela Média) ---")
    guardiao.verificar_data_drift([10.0, 45.0, 5.0, 44.0], [70.0, 72.0, 68.0, 70.0])
    
    print("\n" + "="*60 + "\n")
    
    print("=== FASE 2: TESTES METAMÓRFICOS (COMPORTAMENTO DA IA) ===")
    
    print("\n--- Cenário Metamórfico A: Operação Segura ---")
    guardiao.testar_relacao_metamorfica_umidade(temp_fixa=30.0, umidade_base=50.0)
    
    print("\n--- Cenário Metamórfico B: Iminência do Extremo ---")
    guardiao.testar_relacao_metamorfica_umidade(temp_fixa=35.0, umidade_base=75.0)

    print("\n--- Cenário Metamórfico C: Nova Suite de Teste de Temperatura ---")
    guardiao.testar_relacao_metamorfica_temperatura(umidade_fixa=88.0, temp_base=35.0)