import React, {useState} from 'react';
import style from './Form.module.css';
import doFetch from "../services/doFetch";

const Form = () => {

    const [numberOfPopulation, setNumberOfPopulation] = useState(0);
    const [lengthOfChromosome, setLengthOfChromosome] = useState(0);
    const [epochs, setEpochs] = useState(0);
    const [crossProbability, setCrossProbability] = useState(0);
    const [inversionProbability, setInversionProbability] = useState(0);
    const [selectionBestPercent, setSelectionBestPercent] = useState(0);
    const [elitistStrategyPercent, setElitistStrategyPercent] = useState(0);

    const parameters = {
        numberOfPopulation,
        lengthOfChromosome,
        epochs,
        crossProbability,
        inversionProbability,
        selectionBestPercent,
        elitistStrategyPercent
    }

    const send = (event) => {
        event.preventDefault()
        return doFetch("http://localhost:8000/classic-EA/", "POST", parameters)
            .then(response => {
                if (!response.ok) {
                    throw Error('Błędne żądanie!');
                }
                return response.json();
            })
    }

    return (
        <div>
            <h2>Parameters</h2>
            <form className={style.form} onSubmit={send}>
                <label className={style.formLabel}>Number of population</label>
                <div className={style.formInputs}>
                    <input
                        className={style.formInput}
                        type='number'
                        required={true}
                        value={numberOfPopulation}
                        onChange={(e) => setNumberOfPopulation(e.target.value)}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Length of chromosome</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={lengthOfChromosome}
                        onChange={(e => setLengthOfChromosome(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Epochs</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={epochs}
                        min={0}
                        max={100}
                        onChange={(e => setEpochs(e.target.value))}
                    />
                </div> <div className={style.formInputs}>
                    <label className={style.formLabel}>Cross probability</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={crossProbability}
                        min={0}
                        max={100}
                        onChange={(e => setCrossProbability(e.target.value))}
                    />
                </div> <div className={style.formInputs}>
                    <label className={style.formLabel}>Inversion Probability</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={inversionProbability}
                        min={0}
                        max={100}
                        onChange={(e => setInversionProbability(e.target.value))}
                    />
                </div> <div className={style.formInputs}>
                    <label className={style.formLabel}>Selection best percent</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={selectionBestPercent}
                        min={0}
                        max={100}
                        onChange={(e => setSelectionBestPercent(e.target.value))}
                    />
                </div> <div className={style.formInputs}>
                    <label className={style.formLabel}>Elitist Strategy Percent</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={elitistStrategyPercent}
                        min={0}
                        max={100}
                        onChange={(e => setElitistStrategyPercent(e.target.value))}
                    />
                </div>
                <button type='submit'>
                    Go
                </button>
            </form>
        </div>
    );
};

export default Form;
