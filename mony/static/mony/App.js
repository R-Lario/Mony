function getCookie(name) {
    if (!document.cookie) {
        return null;
    }

    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
        return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

function setCookie(cname, cvalue, clifetime) {
    var d = new Date();
    d.setTime(d.getTime() + (clifetime * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function accessTokenHandler(setTokensLoaded = 0) {
    let accessToken, refreshToken;
    async function refreshAccessToken(refreshToken) {
        let csrf_token = getCookie("csrftoken");
        let response = await fetch("/api/refresh-access-token", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                "refreshToken": refreshToken
            })
        });
        let data = await response.json();
        // check if tokens could be refreshed
        if (response.status == 200) {
            setCookie("accessToken", data.access, data.access_expires);
            if (setTokensLoaded) {
                setTokensLoaded(true);
            }
        } else {
            console.log(data);
            getNewTokens();
        }
    }

    async function getNewTokens() {
        let response = await fetch("api/get-new-access-token");
        let result = await response.json();
        setCookie("accessToken", result.access, result.access_expires);
        setCookie("refreshToken", result.refresh, result.refresh_expires);
        if (setTokensLoaded) {
            setTokensLoaded(true);
        }
    }
    accessToken = getCookie("accessToken");
    refreshToken = getCookie("refreshToken");

    // IF ACCESSTOKEN IS EXPIRED, BUT REFRESHTOKEN ISN'T
    if (!accessToken && refreshToken) {
        refreshAccessToken(refreshToken);
    } else if (!accessToken && !refreshToken) {
        getNewTokens();
    }
    else {
        if (setTokensLoaded) {
            setTokensLoaded(true);
        }
    }
}


///////////////////////////////////////


function ConnectBank() {
    let [stepCount, setStepCount] = React.useState(0);
    let [selectedCountry, setSelectedCountry] = React.useState();
    let [bankList, setBankList] = React.useState([]);
    let [selectedBankHTML, setSelectedBankHTML] = React.useState();
    let [selectedBankName, setSelectedBankName] = React.useState();
    let [bankConnectLink, setBankConnectLink] = React.useState();
    let [userAgreementCard, setUserAgreementCard] = React.useState("Loading...");


    React.useEffect(() => {
        accessTokenHandler();
    });

    React.useEffect(() => {
        if (selectedCountry) {
            getBanks();
        }
    }, [selectedCountry]);

    React.useEffect(() => {
        if (selectedBankHTML) {
            setSelectedBankName(selectedBankHTML.querySelector("a").innerHTML);
        }
    }, [selectedBankHTML]);

    React.useEffect(() => {
        if (selectedBankName) {
            buildLink();
        }
    }, [selectedBankName]);

    React.useEffect(() => {
        if (bankConnectLink) {
            buildUserAgreement();
        }
    }, [bankConnectLink]);


    function countrySelect() {
        let countryList = {
            "AT": "Austria",
            "BE": "Belgium",
            "BG": "Bulgaria",
            "HR": "Croatia",
            "CY": "Cyprus",
            "CZ": "Czech Republic",
            "DK": "Denmark",
            "EE": "Estonia",
            "FI": "Finland",
            "FR": "France",
            "DE": "Germany",
            "GR": "Greece",
            "HU": "Hungary",
            "IS": "Iceland",
            "IE": "Ireland",
            "IT": "Italy",
            "LV": "Latvia",
            "LT": "Lithuania",
            "LI": "Liechtenstein",
            "LU": "Luxembourg",
            "MT": "Malta",
            "NL": "The Netherlands",
            "NO": "Norway",
            "PL": "Poland",
            "PT": "Portugal",
            "RO": "Romania",
            "SK": "Slovakia",
            "SI": "Slovenia",
            "ES": "Spain",
            "SE": "Sweden",
            "UK": "United Kindom"
        }

        function handleChange(event) {
            setSelectedCountry(event.currentTarget.value);
            setStepCount(prevStep => prevStep + 1);
        }
        return (
            <div>
                <select class="form-select" onChange={handleChange}>
                    <option disabled selected value>Select your banks country</option>
                    {Object.entries(countryList).map(([key, value]) => (
                        <option value={key}>{value}</option>
                    ))}
                </select>
            </div>
        );
    }

    function bankSelectClickHandler(event) {
        setStepCount(prevStep => prevStep + 1);
        setSelectedBankHTML(event.currentTarget);
    }

    async function getBanks() {

        let accessToken = getCookie("accessToken");
        let response = await fetch(`api/get-banks/${selectedCountry}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `${accessToken}`
            }
        });
        let result = await response.json();

        setBankList(result);
    }

    async function buildLink() {
        //first part
        let csrf_token = getCookie('csrftoken');
        let accessToken = getCookie("accessToken");
        let selectedBank = selectedBankHTML.id;
        let response = await fetch("api/create-user-agreement", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': accessToken,
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                "institution_id": selectedBank
            })
        });
        let data = await response.json();
        let agreementId = data.id;
        let imageUrl = selectedBankHTML.querySelector("img").src;

        //STEP 1 REQ OPTIONAL
        response = await fetch("api/handle-requisition-confirmation/set-agreement-id", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({
                "agreement_id": agreementId,
                "bank_name": selectedBankName,
                "image_url": imageUrl
            })
        });
        data = await response.json();
        let requisitionConfirmationUrl = window.location.origin + "/api/handle-requisition-confirmation/confirm-agreement/" + agreementId;
        console.log(requisitionConfirmationUrl);

        //second part
        response = await fetch("api/build-link", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': accessToken,
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                "institution_id": selectedBank,
                "redirect": requisitionConfirmationUrl,
                "agreement": agreementId
            })
        });
        data = await response.json();
        setBankConnectLink(data.link);
        // STEP 2 REQ OPTIONAL
        let requisitionId = data.id;
        response = await fetch("api/handle-requisition-confirmation/bind-requisition", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({
                "agreement_id": agreementId,
                "requisition_id": requisitionId
            })
        });
        data = await response.json();
    }


    function buildUserAgreement() {
        setUserAgreementCard(
            <div class="card">
                <div class="card-header">
                    Connect your bank account
                </div>
                <div class="card-body">
                    <h5 class="card-title">Connect your {selectedBankName} account.</h5>
                    <a href={bankConnectLink} class="btn btn-primary" target="_blank">Connect</a>
                </div>
            </div>);
    }

    return (
        <>
            <h2>Connect your bank account</h2>
            {stepCount > 0 && <button type="button" class="btn btn-primary w-100 mb-3" onClick={() => { setStepCount(stepCount - 1) }}>Go back</button>}

            {stepCount == 0 && countrySelect()}

            {(stepCount == 1 && bankList.length == 0) && <p>Loading...</p>}
            {stepCount == 1 && (
                <div style={{ maxHeight: "300px", overflowY: "scroll", overflowX: "hidden" }}>
                    {bankList.map(item => (
                        <div id={item.id} class="container-fluid my-2 border-top py-2" onClick={bankSelectClickHandler}>
                            <img height="50px" width="50px" src={item.logo} />
                            <a class="text-decoration-none ms-2">{item.name}</a>
                        </div>
                    )
                    )}
                </div>
            )}

            {stepCount == 2 && userAgreementCard}

        </>
    );
}

function TransactionCategory(props) {
    let csrfToken = getCookie("csrftoken");

    let [categories, setCategories] = React.useState([]);

    React.useEffect(async () => {
        let response = await fetch("/api/category");
        let data = await response.json();
        setCategories(data);
    }, []);

    async function reloadCategories() {
        let response = await fetch("/api/category");
        let data = await response.json();
        setCategories(data);

        props.transactionsRefresh();
    }

    async function handleSubmit(event) {
        event.preventDefault();
        let category = event.currentTarget.category.value;
        event.currentTarget.category.value = "";
        let response = await fetch("/api/category", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "category": category
            })
        });
        let data = await response.json();
        reloadCategories();
    }

    async function handleClick(event) {
        let category = event.currentTarget.parentNode.parentNode.querySelector(".category-text").innerHTML;
        let response = await fetch("/api/category", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                category: category
            })
        });
        let data = await response.json();
        reloadCategories();
    }

    return (
        <>
            <h2>Add and delete categories</h2>
            <form method="POST" onSubmit={handleSubmit}>
                <div class="input-group w-md-75 text-center">
                    <input class="form-control" placeholder="Category" type="text" name="category" required autocomplete="off" />
                    <button class="input-group-text" type="submit">Submit</button>
                </div>

            </form>
            <div class="mt-3" style={{ maxHeight: "300px", overflowY: "scroll", overflowX: "hidden" }}>
                {categories.length == 0 && <p>Loading...</p>}
                {categories.length > 0 && categories.map(item => (
                    <div class="row row-striped my-1 py-2 px-0 w-100">
                        <div class="col">
                            <a class="ps-2 text-decoration-none text-dark category-text">{item.category}</a>
                        </div>
                        <div class="col-auto">
                            <button class="btn btn-danger" onClick={handleClick}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
}

function Transaction(props) {
    React.useEffect(() => {
        accessTokenHandler();
    });
    async function updateTransactionCategory(transactionId, category) {
        let csrfToken = getCookie("csrftoken");
        let response = await fetch("/api/set-transaction-category", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "category": category,
                "transaction_id": transactionId
            })
        });
        let data = await response.json();
        props.googleDiagramsRefresh();
    }
    function changeHandler(event) {
        let value = event.currentTarget.value;
        let id = event.currentTarget.id;
        updateTransactionCategory(id, value);
    }
    let category = props.item.category ? props.item.category.category : "No selected category";

    return (
        <tr>
            <td>{props.item.date}</td>
            <td>{props.item.transaction_amount} {props.item.currency}</td>
            <td>{props.item.description}</td>
            <td>
                <select id={props.item.transaction_id} name="category" onChange={changeHandler} class="form-select">
                    <option disabled {...(props.item.category ? {} : { selected: true })} value>Transaction category</option>

                    {props.categories.map(item =>
                        (<option {...(category == item.category ? { selected: true } : {})} value={item.category}>{item.category}</option>)
                    )
                    }
                </select>
            </td>
        </tr>
    );
}

function TransactionHistory(props) {
    let [requisitions, setRequisitions] = React.useState([]);
    let [transactions, setTransactions] = React.useState([]);
    let [categories, setCategories] = React.useState([]);

    React.useEffect(() => {
        props.setTransactionsRefresh(() => refresh);
        refresh();
    }, []);


    React.useEffect(() => {
        if (requisitions.length > 0) {
            getAllTransactions();
        }
    }, [requisitions]);

    async function refresh() {
        let response = await fetch('/api/requisitions');
        let data = await response.json();
        getUserCategories()
        setRequisitions(data);

        if (props.googleDiagramsRefresh) {
            props.googleDiagramsRefresh();
        }
    }

    async function getAllTransactions() {
        let authToken = getCookie("accessToken");

        let response = await fetch("/api/get-transactions", {
            headers: {
                "Authorization": authToken
            }
        });
        let data = await response.json();
        setTransactions(data);
    }

    async function getUserCategories() {
        let response = await fetch("/api/category");
        let data = await response.json();
        setCategories(data);
    }

    async function removeBankAccount(event) {
        let csrfToken = getCookie("csrftoken");
        let requisition_id = event.currentTarget.parentNode.parentNode.id;
        console.log(requisition_id);
        let response = await fetch("/api/requisitions/" + requisition_id, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken
            }
        });
        let data = await response.json();
        console.log(data);

        refresh();
    }

    return (
        <>
            <h2>Transaction history</h2>

            {requisitions.length > 0 && (
                <>
                    <p>Selected banks:</p>
                    {requisitions.map(item => (
                        <div id={item.requisition_id} class="row my-1">
                            <div class="col">
                                <a><img height="35px" width="35px" src={item.image_url} /><span id="bank_name">{item.bank_name}</span></a>
                            </div>
                            <div class="col-auto">
                                <button class="btn btn-danger" onClick={removeBankAccount}>Remove bank account</button>
                            </div>

                        </div>
                    )
                    )}
                </>
            )}

            {transactions.length == 0 && <p>Loading transactions...</p>}

            {transactions.length > 0 && (
                <div style={{ overflowX: "scroll", overflowY: "scroll", maxHeight: "400px" }}>
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Amount</th>
                                <th>Description</th>
                                <th>Category</th>
                            </tr>
                        </thead>
                        <tbody>
                            {transactions.map(item => (
                                <Transaction
                                    item={item}
                                    categories={categories}
                                    googleDiagramsRefresh={props.googleDiagramsRefresh}
                                />
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </>

    );
}

function GoogleDiagrams(props) {
    google.charts.load('current', { 'packages': ['corechart'] });

    let [months, setMonths] = React.useState([]);
    let [selectedMonth, setSelectedMonth] = React.useState();
    let [monthsData, setMonthsData] = React.useState();
    let [categories, setCategories] = React.useState([]);
    let [screenWidth, setScreenWidth] = React.useState(screen.width);
    let [height, setHeight] = React.useState();

    React.useEffect(() => {
        props.setGoogleDiagramsRefresh(() => refresh);
        setScreenWidth(screen.width);
        refresh();
    }, []);

    React.useEffect(() => {
        if (screenWidth < 400) {
            setHeight("300px");
        }
        else if (screenWidth < 600) {
            setHeight("350px");
        }
        else if (screenWidth < 1600) {
            setHeight("400px");
        }
        else {
            setHeight("500px");
        }
    }, [screenWidth, height]);


    React.useEffect(() => {
        if (months.length && categories.length) {

            //THIS WILL LOAD THE SELECTED PIEDIAGRAM
            handleChange({ currentTarget: { value: months[0] } });

            //THIS LOADS THE BAR DIAGRAM
            drawLineGraph();

            //THIS LOADS THE LINE CATEGORY GRAPH
            drawBarDiagram();
        }
    }, [months, categories]);


    React.useEffect(() => {
        if (months.length > 0) {
            let allDivs = document.querySelectorAll(".montly-category-spending");
            allDivs.forEach(item => {
                item.classList.add("d-none");
            });

            let div = document.querySelector("#" + selectedMonth);
            
            div.classList.remove("d-none");
            drawPieDiagram(selectedMonth);
        }
    }, [selectedMonth]);


    function refresh() {
        loadSpendingData();
        getCategories();
    }

    async function getCategories() {
        let response = await fetch("/api/category");
        let data = await response.json();
        setCategories(data);
    }

    function getMonthlySpendingPerCategory(monthlyData, categories) {

        let arr = categories.map(category => {
            if (monthlyData[category]) {
                return monthlyData[category];
            }
            else {
                return 0;
            }
        });

        return arr;
    }

    async function loadSpendingData() {
        let response = await fetch("/api/data/category-spending");
        let data = await response.json();
        let months = Object.keys(data);
        months = months.map(month => month.replace(" ", "-"));

        setMonthsData(data);
        setMonths(months);
    }

    function drawPieDiagram(id) {
        let div = document.querySelector("#" + id);
        let key = id.replace("-", " ");
        let monthData = monthsData[key];

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Category');
        data.addColumn('number', 'Amount');

        data.addRows(
            Object.entries(monthData).map(([key, value]) => [key, value])
        );

        // Set chart options
        var options = {
            'width': 'auto',
            'height': height,
            'title': `Transactions per category (${key})`,
        };


        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(div);

        chart.draw(data, options);
    }

    function drawBarDiagram() {
        let div = document.querySelector('#google-stacked-bar-chart');


        let monthList = months.map(month => month.replace('-', ' '));
        let categoryList = categories.map(category => category.category);


        let diagramData = monthList.map(month => [month, ...getMonthlySpendingPerCategory(monthsData[month], categoryList), '']);

        var data = google.visualization.arrayToDataTable([
            ['Month', ...categoryList, { role: 'annotation' }],
            ...diagramData
        ]);

        var options = {
            'width': 'auto',
            'height': height,
            title: 'Monthly spending per category',
            legend: { position: 'bottom', maxLines: 3 },
            bar: { groupWidth: '75%' },
            isStacked: true
        };

        var view = new google.visualization.DataView(data);

        var chart = new google.visualization.ColumnChart(div);
        chart.draw(view, options);
    }

    function drawLineGraph() {
        let div = document.querySelector("#google-curve-chart");


        let monthList = months.map(month => month.replace('-', ' '));
        let categoryList = categories.map(category => category.category);


        let diagramData = monthList.map(month => [month, ...getMonthlySpendingPerCategory(monthsData[month], categoryList), '']);

        var data = google.visualization.arrayToDataTable([
            ['Month', ...categoryList, { role: 'annotation' }],
            ...diagramData
        ]);

        var options = {
            'width': 'auto',
            'height': height,
            title: 'Monthly spendings per category',
            legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(div);

        chart.draw(data, options);
    }

    function handleChange(event) {
        let id = event.currentTarget.value;
        setSelectedMonth(id);
    }

    return (
        <>
            <div id="google-pie-chart" class="col-12 col-lg-4 p-0">
                {months.map(item => <div id={item} class="montly-category-spending p-0" style={{ height: height }}></div>)}
                <select value={selectedMonth} onChange={handleChange} class="form-select">
                    {months.map(item => (
                        <option value={item}>{item.replace('-', ' ')}</option>
                    ))}
                </select>
            </div>
            <div id="google-curve-chart" class="col-12 col-lg-4 p-0" style={{ height: height }}></div>
            <div id="google-stacked-bar-chart" class="col-12 col-lg-4 p-0" style={{ height: height }}></div>
        </>
    );
}

function App() {
    let [transactionsRefresh, setTransactionsRefresh] = React.useState(() => () => console.log("Refresh..."));
    let [googleDiagramsRefresh, setGoogleDiagramsRefresh] = React.useState();
    let [tokensLoaded, setTokensLoaded] = React.useState(false);

    React.useEffect(() => {
        accessTokenHandler(setTokensLoaded);
    }, []);


    return (
        <>
            {!tokensLoaded && <a>Loading...</a>}
            {tokensLoaded && (
                <>
                    <div id="google-charts" class="container-fluid row p-0 m-0">
                        <GoogleDiagrams setGoogleDiagramsRefresh={setGoogleDiagramsRefresh} />
                    </div>
                    <div class="row">
                        <div class="col-12 col-lg-6" id="transaction-category">
                            <TransactionCategory transactionsRefresh={transactionsRefresh} />
                        </div>
                        <hr class="d-lg-none my-3" />
                        <div class="col-12 col-lg-6" id="connect-bank">
                            <ConnectBank />
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col" id="transaction-history">
                            <TransactionHistory
                                setTransactionsRefresh={setTransactionsRefresh}
                                googleDiagramsRefresh={googleDiagramsRefresh}
                            />
                        </div>
                    </div>
                </>
            )}

        </>
    );
}


ReactDOM.render(<App />, document.querySelector("#App"));