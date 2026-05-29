import numpy as np

# =====================================================================
# 1. FRAMEWORK DE IA: MODELO BAYESIANO SIMULADO
# =====================================================================
def modelo_bayesiano_risco_clima(temperatura: float, umidade: float) -> float:
    """
    Simula uma rede Bayesiana que calcula a probabilidade (0% a 100%) 
    de um evento climático extremo baseado em Temperatura e Umidade.
    """
    # Validação física dos sensores (Requisito Funcional)
    if not (0 <= temperatura <= 50) or not (0 <= umidade <= 100):
        raise ValueError("Leitura dos sensores fora dos limites físicos da Terra.")

    # Fator de instabilidade termodinâmica simplificado
    fator_termico = temperatura / 40.0
    fator_umidade = umidade / 100.0
    
    # Lógica Probabilística Bayesiana Normal
    if umidade <= 85.0:
        # Quanto maior a temperatura e maior a umidade, maior o risco de tempestade
        probabilidade = (fator_termico * 0.4 + fator_umidade * 0.6) * 100
        return min(max(probabilidade, 0.0), 100.0)
    else:
        # ❌ BUG OCULTO SILENCIOSO (Erro de inversão de sinal em umidade extrema)
        # Em vez de somar o risco do ar saturado, o modelo subtrai erroneamente.
        probabilidade = (fator_termico * 0.4 - (fator_umidade * 1.2)) * 100
        return max(probabilidade, 0.0)


# =====================================================================
# 2. MOTOR DE ENGENHARIA DE QUALIDADE (QA & SRE)
# =====================================================================
class GuardiaoQualidadeIA:
    def __init__(self):
        # Padrões históricos aceitáveis para a região (Florianópolis/Joinville)
        self.limite_superior_temp = 38.0
        self.limite_inferior_umidade = 20.0

    def verificar_data_drift(self, lote_temperaturas: list, lote_umidades: list) -> bool:
        """CONCEITO: Avalia se os dados de produção sofreram desvio estatístico perigoso"""
        media_temp = float(np.mean(lote_temperaturas))
        media_umi = float(np.mean(lote_umidades))
        
        print(f"-> Analisando Lote - Média Temp: {media_temp:.1f}°C | Média Umidade: {media_umi:.1f}%")
        
        # Alerta se as médias fugirem completamente do clima histórico regional
        if media_temp > self.limite_superior_temp or media_umi < self.limite_inferior_umidade:
            print("❌ [ALERTA DE QUALIDADE] Data Drift Detectado! Clima fora do padrão de treino da IA.")
            return False
            
        print("✅ [SUCESSO] Dados aprovados no teste de consistência estocástica.")
        return True

    def testar_relacao_metamorfica(self, temp_fixa: float, umidade_base: float) -> bool:
        """
        CONCEITO: Se a umidade aumenta e a temperatura continua alta, 
        o risco probabilístico calculado pela IA DEVE obrigatoriamente aumentar (ou se manter).
        """
        umidade_elevada = umidade_base + 15.0  # Incrementa a umidade para o teste
        
        # Executa a IA para os dois cenários (Par metamórfico)
        risco_base = modelo_bayesiano_risco_clima(temp_fixa, umidade_base)
        risco_alto = modelo_bayesiano_risco_clima(temp_fixa, umidade_elevada)
        
        print(f"\n[Teste Metamórfico] Mantendo {temp_fixa}°C fixos:")
        print(f"   * Cenário A (Umidade {umidade_base:.1f}%): Risco de Desastre = {risco_base:.1f}%")
        print(f"   * Cenário B (Umidade {umidade_elevada:.1f}%): Risco de Desastre = {risco_alto:.1f}%")
        
        # Validação da regra de qualidade matemática
        if risco_alto >= risco_base:
            print("✅ [SUCESSO] Propriedade Metamórfica Mantida. IA agindo de forma lógica.")
            return True
        else:
            print("❌ [BUG CRÍTICO DETECTADO] O ar saturou de umidade, mas o risco calculado CAIU! A IA alucinou.")
            return False


# =====================================================================
# 3. EXECUÇÃO DOS CENÁRIOS DE TESTE
# =====================================================================
if __name__ == "__main__":
    guardiao = GuardiaoQualidadeIA()
    
    print("=== FASE 1: TESTES DE DATA DRIFT (ENTRADA DE DADOS) ===")
    
    # Caso 1: Clima típico de Santa Catarina
    print("\n--- Testando Lote 1 (Sensores Normais) ---")
    temps_1 = [22.5, 24.0, 23.1, 25.8]
    umis_1 = [70.0, 75.5, 72.0, 68.0]
    guardiao.verificar_data_drift(temps_1, umis_1)
    
    # Caso 2: Sensores reportando uma onda de calor saariana inédita (Drift)
    print("\n--- Testando Lote 2 (Anomalia Térmica / Mudança Climática) ---")
    temps_2 = [42.0, 44.5, 41.2, 43.0]
    umis_2 = [15.0, 12.5, 18.0, 14.2]
    guardiao.verificar_data_drift(temps_2, umis_2)
    
    print("\n" + "="*60 + "\n")
    
    print("=== FASE 2: TESTES METAMÓRFICOS (COMPORTAMENTO DA IA) ===")
    
    # Cenário Metamórfico A: Testando em faixas seguras de operação
    # Se a umidade sobe de 50% para 65% com 30°C fixos, o risco deve subir.
    guardiao.testar_relacao_metamorfica(temp_fixa=30.0, umidade_base=50.0)
    
    # Cenário Metamórfico B: Testando na iminência do extremo (Gatilho do Bug)
    # Se a umidade sobe de 75% para 90% com 35°C fixos, o risco deveria explodir, mas...
    guardiao.testar_relacao_metamorfica(temp_fixa=35.0, umidade_base=75.0)