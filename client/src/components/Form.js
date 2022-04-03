import React, {useState} from 'react';
import style from './Form.module.css';
import doFetch from "../services/doFetch";

const Form = () => {

    const [numberOfPopulation, setNumberOfPopulation] = useState(0)
    const [lengthOfChromosome, setLengthOfChromosome] = useState(0)
    const [epochs, setEpochs] = useState(0)
    const [crossProbability, setCrossProbability] = useState(0)
    const [mutationProbability, setMutationProbability] = useState(0)
    const [inversionProbability, setInversionProbability] = useState(0)
    const [selectionPercent, setSelectionPercent] = useState(0)
    const [elitistStrategyPercent, setElitistStrategyPercent] = useState(0)
    const [sizeOfTournament, setSizeOfTournament] = useState(0)
    const [selectionName, setSelectionName] = useState("best")
    const [crossoverName, setCrossoverName] = useState("onePoint")
    const [mutationName, setMutationName] = useState("edge")

    const parameters = {
        numberOfPopulation,
        lengthOfChromosome,
        epochs,
        crossProbability,
        mutationProbability,
        inversionProbability,
        selectionPercent,
        elitistStrategyPercent,
        sizeOfTournament,
        selectionName,
        crossoverName,
        mutationName
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
                        onChange={(e => setEpochs(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Cross probability</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={crossProbability}
                        step={"0.01"}
                        onChange={(e => setCrossProbability(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Mutation probability</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={mutationProbability}
                        step={"0.01"}
                        onChange={(e => setMutationProbability(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Inversion Probability</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={inversionProbability}
                        step={"0.01"}
                        onChange={(e => setInversionProbability(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Selection best percent</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={selectionPercent}
                        step={"0.01"}
                        onChange={(e => setSelectionPercent(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Elitist Strategy Percent</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={elitistStrategyPercent}
                        step={"0.01"}
                        onChange={(e => setElitistStrategyPercent(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Size of Tournament</label>
                    <input
                        className={style.formInput}
                        type='number'
                        value={sizeOfTournament}
                        max={numberOfPopulation}
                        onChange={(e => setSizeOfTournament(e.target.value))}
                    />
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Selection Name</label>
                    <select value={selectionName}
                            onChange={(e => setSelectionName(e.target.value))}
                            className={style.formInput}
                    >
                        <option value={"best"}>Best</option>
                        <option value={"roulette"}>Roulette</option>
                        <option value={"tournament"}>Tournament</option>
                    </select>
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Crossover Name</label>
                    <select value={crossoverName}
                            onChange={(e => setCrossoverName(e.target.value))}
                            className={style.formInput}
                    >
                        <option value={"one_point"}>One point</option>
                        <option value={"two_points"}>Two points</option>
                        <option value={"three_points"}>Three points</option>
                        <option value={"uniform"}>Uniform</option>
                    </select>
                </div>
                <div className={style.formInputs}>
                    <label className={style.formLabel}>Mutation Name</label>
                    <select value={mutationName}
                            onChange={(e => setMutationName(e.target.value))}
                            className={style.formInput}
                    >
                        <option value={"edge"}>Edge</option>
                        <option value={"one_point"}>One point</option>
                        <option value={"two_points"}>Two points</option>
                    </select>
                </div>
                <button type='submit'>
                    Start
                </button>
            </form>
        </div>
    );
};

export default Form;
