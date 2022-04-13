import React, {useState} from 'react';
import style from './Form.module.css';
import doFetch from "../services/doFetch";

const Form = () => {

    const [numberOfPopulation, setNumberOfPopulation] = useState(0)
    const [epochs, setEpochs] = useState(0)
    const [crossProbability, setCrossProbability] = useState(0)
    const [mutationProbability, setMutationProbability] = useState(0)
    const [selectionPercent, setSelectionPercent] = useState(0)
    const [elitistStrategyPercent, setElitistStrategyPercent] = useState(0)
    const [sizeOfTournament, setSizeOfTournament] = useState(0)
    const [selectionName, setSelectionName] = useState("best")
    const [crossoverName, setCrossoverName] = useState("arithmetic")
    const [mutationName, setMutationName] = useState("uniform")

    const parameters = {
        numberOfPopulation,
        epochs,
        crossProbability,
        mutationProbability,
        selectionPercent,
        elitistStrategyPercent,
        sizeOfTournament,
        selectionName,
        crossoverName,
        mutationName
    }

    const send = (event) => {
        event.preventDefault()
        return doFetch("http://localhost:8000/EA-real_chromosome/", "POST", parameters)
            .then(response => {
                if (!response.ok) {
                    window.alert('Bad request!')
                    throw Error('Bad request');
                }
                return response.json();
            })
            .then(data => {
                window.alert("Status: OK\nExecution time: " + data.time + " s")
            })
    }

    return (
        <div className={style.content}>
            <h2>Parameters</h2>
            <div className={style.flexContainer}>
                <form className={style.form}>
                    <div className={style.formInputs}>
                        <label className={style.formLabel}>Number of population</label>
                        <input
                            className={style.formInput}
                            type='number'
                            required={true}
                            value={numberOfPopulation}
                            onChange={(e) => setNumberOfPopulation(e.target.value)}
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
                        <label className={style.formLabel}>Selection percent</label>
                        <input
                            className={style.formInput}
                            type='number'
                            value={selectionPercent}
                            step={"0.01"}
                            onChange={(e => setSelectionPercent(e.target.value))}
                        />
                    </div>
                </form>
                <form className={style.form}>
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
                            <option value={"arithmetic"}>Arithmetic</option>
                            <option value={"linear"}>Linear</option>
                            <option value={"blend_alpha"}>Blend alpha</option>
                            <option value={"blend_alpha_beta"}>Blend alpha-beta</option>
                            <option value={"average"}>Average</option>
                        </select>
                    </div>
                    <div className={style.formInputs}>
                        <label className={style.formLabel}>Mutation Name</label>
                        <select value={mutationName}
                                onChange={(e => setMutationName(e.target.value))}
                                className={style.formInput}
                        >
                            <option value={"uniform"}>Uniform</option>
                            <option value={"gauss"}>Gauss</option>
                        </select>
                    </div>
                </form>
            </div>
            <button onClick={send}>
                Start
            </button>
        </div>
    );
};

export default Form;
