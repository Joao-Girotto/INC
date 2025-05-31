# Extração de Características de Sinais EMG

Este projeto processa sinais EMG, realizando etapas de pré-processamento, filtragem, segmentação em janelas e extração de características no domínio do tempo e da frequência. O objetivo é preparar os dados para tarefas posteriores, como classificação por aprendizado de máquina.

## O que o código faz

1. Carregamento de Dados: Três arquivos `.npy` contendo dados de EEG são carregados e combinados em uma única matriz.
2. Filtragem de Sinais: São aplicados filtros:
   - Band-pass (passa-faixa de 5–50 Hz)
   - Notch para remover ruído da rede elétrica (60 Hz)
3. Segmentação em Janelas: O sinal é dividido em janelas temporais e espectrais (via STFT).
4. Extração de Características: São extraídas features como:
   - No domínio do tempo: variância, RMS, comprimento da linha, número de cruzamentos por zero.
   - No domínio da frequência: densidade espectral de potência (PSD), frequência média, entre outras.

## Bibliotecas utilizadas

| Biblioteca             | Finalidade                                                                 |
|------------------------|---------------------------------------------------------------------------|
| numpy                  | Manipulação eficiente de arrays.                                           |
| scipy.signal           | Aplicação de filtros e transformada de Fourier de curto tempo (STFT).      |
| matplotlib.pyplot      | (Importada, mas não utilizada nas células analisadas).                     |
| sklearn.decomposition  | PCA (foi importado, mas ainda não utilizado no trecho visível).            |
| sklearn.svm            | SVM (foi importado, mas não utilizado até o trecho analisado).             |
| copy.deepcopy          | Evitar modificação in-place dos dados após filtragem.                      |
| math.prod              | Cálculo do produto de dimensões para normalização nas features.            |

## Estrutura esperada

Os dados devem estar disponíveis em um diretório `dataset/`, com os arquivos:

```
dataset/
├── s03_1.npy
├── s03_2.npy
├── s03_3.npy
```

## Como executar

1. Clone ou baixe o repositório.
2. Certifique-se de ter os arquivos `.npy` no diretório `dataset/`.
3. Instale as dependências com:

```bash
pip install numpy scipy scikit-learn matplotlib
```

4. Execute o notebook:

```bash
jupyter notebook experiment.ipynb
```

5. Execute célula por célula para processar os dados e extrair as características.

## Status

O código já realiza:

- Carregamento e combinação de sinais.
- Filtragem band-pass e notch.
- Segmentação dos dados.
- Extração de features básicas.

Próximos passos podem incluir:

- Treinamento de modelos de ML com as features extraídas.
- Visualização dos dados e análise estatística.
