import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [activeSection, setActiveSection] = useState("overview");

  const [metrics, setMetrics] = useState(null);
  const [riskResults, setRiskResults] = useState([]);
  const [highRisk, setHighRisk] = useState([]);

  const [customerId, setCustomerId] = useState("");
  const [investigation, setInvestigation] = useState(null);

  const [loading, setLoading] = useState(true);
  const [investigating, setInvestigating] = useState(false);
  const [error, setError] = useState("");

  // ============================================================
  // Load dashboard data
  // ============================================================

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [
        metricsRes,
        riskRes,
        highRiskRes
      ] = await Promise.all([
        axios.get(`${API}/dashboard/metrics`),
        axios.get(`${API}/risk-results`),
        axios.get(`${API}/risk-results/high`)
      ]);

      setMetrics(metricsRes.data);
      setRiskResults(riskRes.data.results || []);
      setHighRisk(highRiskRes.data.results || []);

    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to the Credixis API. Make sure FastAPI is running."
      );

    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // Navigation
  // ============================================================

  function navigateTo(section) {
    setActiveSection(section);
  }

  // ============================================================
  // Customer investigation
  // ============================================================

  async function investigateCustomer(e) {
    e.preventDefault();

    if (!customerId.trim()) {
      return;
    }

    try {
      setInvestigating(true);
      setInvestigation(null);

      const response = await axios.get(
        `${API}/fraud-investigation/${customerId.trim()}`
      );

      setInvestigation(response.data);

    } catch (err) {
      console.error(err);

      setInvestigation({
        message: "Customer not found or API request failed."
      });

    } finally {
      setInvestigating(false);
    }
  }

  // ============================================================
  // Helpers
  // ============================================================

  function riskClass(level) {
    if (level === "HIGH") return "risk-high";
    if (level === "MEDIUM") return "risk-medium";
    return "risk-low";
  }

  function formatAmount(amount) {
    return Number(amount || 0).toFixed(2);
  }

  // ============================================================
  // Loading
  // ============================================================

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loader"></div>
        <p>Initializing Credixis Intelligence...</p>
      </div>
    );
  }

  // ============================================================
  // Main application
  // ============================================================

  return (
    <div className="app">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-mark">
            C
          </div>

          <div>
            <h1>Credixis</h1>
            <span>Risk Intelligence</span>
          </div>

        </div>


        <nav>

          {/* Overview */}

          <button
            className={`nav-item ${
              activeSection === "overview" ? "active" : ""
            }`}
            onClick={() => navigateTo("overview")}
          >
            <span>◈</span>
            Overview
          </button>


          {/* Transactions */}

          <button
            className={`nav-item ${
              activeSection === "transactions" ? "active" : ""
            }`}
            onClick={() => navigateTo("transactions")}
          >
            <span>⌁</span>
            Transactions
          </button>


          {/* Risk Monitor */}

          <button
            className={`nav-item ${
              activeSection === "risk" ? "active" : ""
            }`}
            onClick={() => navigateTo("risk")}
          >
            <span>⚠</span>
            Risk Monitor
          </button>


          {/* Investigations */}

          <button
            className={`nav-item ${
              activeSection === "investigations" ? "active" : ""
            }`}
            onClick={() => navigateTo("investigations")}
          >
            <span>◎</span>
            Investigations
          </button>


          {/* Identity Graph */}

          <button
            className={`nav-item ${
              activeSection === "identity" ? "active" : ""
            }`}
            onClick={() => navigateTo("identity")}
          >
            <span>◇</span>
            Identity Graph
          </button>

        </nav>


        {/* Sidebar bottom */}

        <div className="sidebar-bottom">

          <div className="system-status">

            <span className="status-dot"></span>

            <div>
              <strong>Systems operational</strong>
              <small>API connected</small>
            </div>

          </div>

          <div className="version">
            Credixis v1.0
          </div>

        </div>

      </aside>


      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="main">


        {/* ====================================================
            TOP BAR
        ==================================================== */}

        <header className="topbar">

          <div>

            <p className="eyebrow">
              FRAUD INTELLIGENCE PLATFORM
            </p>

            <h2>
              {activeSection === "overview" &&
                "Risk Operations Center"}

              {activeSection === "transactions" &&
                "Transaction Monitor"}

              {activeSection === "risk" &&
                "Risk Monitor"}

              {activeSection === "investigations" &&
                "Fraud Investigations"}

              {activeSection === "identity" &&
                "Identity Graph"}
            </h2>

            <p className="subtitle">

              {activeSection === "overview" &&
                "Monitor transactions, detect anomalies and investigate connected identities."}

              {activeSection === "transactions" &&
                "Review processed transactions and their associated risk signals."}

              {activeSection === "risk" &&
                "Monitor risk scores and review high-risk transactions."}

              {activeSection === "investigations" &&
                "Investigate customer connections and shared identity signals."}

              {activeSection === "identity" &&
                "Explore relationships between customers, devices, IPs and merchants."}

            </p>

          </div>


          <div className="topbar-actions">

            <button
              className="refresh-btn"
              onClick={loadDashboard}
            >
              ↻ Refresh
            </button>

            <div className="live-badge">
              <span></span>
              LIVE
            </div>

          </div>

        </header>


        {/* ====================================================
            ERROR
        ==================================================== */}

        {error && (
          <div className="error-banner">

            <span>!</span>

            {error}

          </div>
        )}


        {/* ====================================================
            OVERVIEW
        ==================================================== */}

        {activeSection === "overview" && metrics && (

          <>

            {/* KPI CARDS */}

            <section className="metrics-grid">

              <div className="metric-card">

                <div className="metric-top">

                  <span>
                    Total transactions
                  </span>

                  <div className="metric-icon blue">
                    ◈
                  </div>

                </div>

                <strong>
                  {metrics.total_transactions.toLocaleString()}
                </strong>

                <small>
                  Processed transaction dataset
                </small>

              </div>


              <div className="metric-card danger-card">

                <div className="metric-top">

                  <span>
                    Fraud detected
                  </span>

                  <div className="metric-icon red">
                    !
                  </div>

                </div>

                <strong>
                  {metrics.fraud_transactions.toLocaleString()}
                </strong>

                <small>
                  {metrics.fraud_rate_percent}%
                  {" "}of total transactions
                </small>

              </div>


              <div className="metric-card">

                <div className="metric-top">

                  <span>
                    Average amount
                  </span>

                  <div className="metric-icon purple">
                    ₹
                  </div>

                </div>

                <strong>
                  ₹
                  {formatAmount(
                    metrics.average_transaction_amount
                  )}
                </strong>

                <small>
                  Average transaction value
                </small>

              </div>


              <div className="metric-card">

                <div className="metric-top">

                  <span>
                    High risk
                  </span>

                  <div className="metric-icon orange">
                    ⚠
                  </div>

                </div>

                <strong>
                  {
                    metrics.processed_risk_distribution
                      ?.HIGH || 0
                  }
                </strong>

                <small>
                  Currently processed risk results
                </small>

              </div>

            </section>


            {/* ANALYTICS */}

            <section className="content-grid">

              <div className="panel risk-panel">

                <div className="panel-header">

                  <div>

                    <p className="panel-label">
                      RISK ANALYTICS
                    </p>

                    <h3>
                      Processed risk distribution
                    </h3>

                  </div>

                  <span className="panel-tag">
                    REAL-TIME
                  </span>

                </div>


                <div className="risk-chart">

                  <div className="risk-bar-container">

                    {(() => {

                      const distribution =
                        metrics.processed_risk_distribution;

                      const total =
                        Object.values(distribution)
                          .reduce(
                            (a, b) => a + b,
                            0
                          );

                      return (
                        <>

                          <div
                            className="risk-bar low"
                            style={{
                              width: `${
                                ((distribution.LOW || 0) /
                                  Math.max(1, total)) *
                                100
                              }%`
                            }}
                          />

                          <div
                            className="risk-bar medium"
                            style={{
                              width: `${
                                ((distribution.MEDIUM || 0) /
                                  Math.max(1, total)) *
                                100
                              }%`
                            }}
                          />

                          <div
                            className="risk-bar high"
                            style={{
                              width: `${
                                ((distribution.HIGH || 0) /
                                  Math.max(1, total)) *
                                100
                              }%`
                            }}
                          />

                        </>
                      );

                    })()}

                  </div>


                  <div className="risk-legend">

                    <div>

                      <span className="legend-dot low-dot"></span>

                      <div>

                        <strong>
                          {
                            metrics
                              .processed_risk_distribution
                              .LOW
                          }
                        </strong>

                        <small>
                          Low risk
                        </small>

                      </div>

                    </div>


                    <div>

                      <span className="legend-dot medium-dot"></span>

                      <div>

                        <strong>
                          {
                            metrics
                              .processed_risk_distribution
                              .MEDIUM
                          }
                        </strong>

                        <small>
                          Medium risk
                        </small>

                      </div>

                    </div>


                    <div>

                      <span className="legend-dot high-dot"></span>

                      <div>

                        <strong>
                          {
                            metrics
                              .processed_risk_distribution
                              .HIGH
                          }
                        </strong>

                        <small>
                          High risk
                        </small>

                      </div>

                    </div>

                  </div>

                </div>

              </div>


              <div className="panel fraud-panel">

                <div className="panel-header">

                  <div>

                    <p className="panel-label">
                      FRAUD SIGNAL
                    </p>

                    <h3>
                      Detection overview
                    </h3>

                  </div>

                  <div className="shield">
                    ✓
                  </div>

                </div>


                <div className="fraud-score">

                  <div className="score-ring">

                    <span>
                      {metrics.fraud_rate_percent}%
                    </span>

                    <small>
                      fraud rate
                    </small>

                  </div>


                  <div className="fraud-copy">

                    <strong>
                      {metrics.fraud_transactions.toLocaleString()}
                    </strong>

                    <span>
                      fraudulent transactions detected
                    </span>

                    <div className="mini-status">

                      <span></span>

                      Monitoring active

                    </div>

                  </div>

                </div>

              </div>

            </section>


            {/* RECENT RESULTS */}

            <RecentTransactions
              riskResults={riskResults}
              formatAmount={formatAmount}
              riskClass={riskClass}
            />

          </>

        )}


        {/* ====================================================
            TRANSACTIONS
        ==================================================== */}

        {activeSection === "transactions" && (

          <section className="panel page-panel">

            <div className="panel-header">

              <div>

                <p className="panel-label">
                  TRANSACTION MONITOR
                </p>

                <h3>
                  Processed transactions
                </h3>

                <p className="panel-description">
                  Transactions that have been processed by
                  the Credixis risk pipeline.
                </p>

              </div>

              <span className="result-count">
                {riskResults.length} results
              </span>

            </div>


            <div className="table-wrapper">

              <table>

                <thead>

                  <tr>

                    <th>
                      Transaction
                    </th>

                    <th>
                      Customer
                    </th>

                    <th>
                      Device
                    </th>

                    <th>
                      Amount
                    </th>

                    <th>
                      Risk score
                    </th>

                    <th>
                      Risk level
                    </th>

                    <th>
                      Fraud
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {riskResults.map((transaction) => (

                    <tr key={transaction.risk_id}>

                      <td className="transaction-id">
                        #{transaction.transaction_id}
                      </td>

                      <td>
                        {transaction.customer_id}
                      </td>

                      <td>
                        {transaction.device_id}
                      </td>

                      <td>
                        ₹
                        {formatAmount(transaction.amount)}
                      </td>

                      <td>

                        <div className="score-cell">

                          <div className="score-line">

                            <span
                              style={{
                                width: `${Math.min(
                                  transaction.risk_score,
                                  100
                                )}%`
                              }}
                            />

                          </div>

                          {transaction.risk_score}

                        </div>

                      </td>

                      <td>

                        <span
                          className={`risk-badge ${riskClass(
                            transaction.risk_level
                          )}`}
                        >
                          {transaction.risk_level}
                        </span>

                      </td>

                      <td>

                        {transaction.is_fraud ? (

                          <span className="fraud-badge">
                            DETECTED
                          </span>

                        ) : (

                          <span className="normal-badge">
                            NORMAL
                          </span>

                        )}

                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </section>

        )}


        {/* ====================================================
            RISK MONITOR
        ==================================================== */}

        {activeSection === "risk" && (

          <>

            {/* Risk metrics */}

            <section className="metrics-grid">

              <div className="metric-card">

                <div className="metric-top">

                  <span>
                    Low risk
                  </span>

                  <div className="metric-icon blue">
                    ✓
                  </div>

                </div>

                <strong>
                  {
                    metrics?.processed_risk_distribution
                      ?.LOW || 0
                  }
                </strong>

                <small>
                  Processed transactions
                </small>

              </div>


              <div className="metric-card">

                <div className="metric-top">

                  <span>
                    Medium risk
                  </span>

                  <div className="metric-icon orange">
                    !
                  </div>

                </div>

                <strong>
                  {
                    metrics?.processed_risk_distribution
                      ?.MEDIUM || 0
                  }
                </strong>

                <small>
                  Requires monitoring
                </small>

              </div>


              <div className="metric-card danger-card">

                <div className="metric-top">

                  <span>
                    High risk
                  </span>

                  <div className="metric-icon red">
                    ⚠
                  </div>

                </div>

                <strong>
                  {
                    metrics?.processed_risk_distribution
                      ?.HIGH || 0
                  }
                </strong>

                <small>
                  Requires investigation
                </small>

              </div>


              <div className="metric-card">

                <div className="metric-top">

                  <span>
                    Risk records
                  </span>

                  <div className="metric-icon purple">
                    ◈
                  </div>

                </div>

                <strong>
                  {riskResults.length}
                </strong>

                <small>
                  Currently processed
                </small>

              </div>

            </section>


            {/* Risk distribution */}

            {metrics && (

              <section className="panel">

                <div className="panel-header">

                  <div>

                    <p className="panel-label">
                      RISK ANALYTICS
                    </p>

                    <h3>
                      Current risk distribution
                    </h3>

                  </div>

                  <span className="panel-tag">
                    LIVE DATA
                  </span>

                </div>


                <div className="risk-chart">

                  <div className="risk-bar-container">

                    {(() => {

                      const d =
                        metrics.processed_risk_distribution;

                      const total =
                        Object.values(d)
                          .reduce(
                            (a, b) => a + b,
                            0
                          );

                      return (
                        <>

                          <div
                            className="risk-bar low"
                            style={{
                              width: `${
                                ((d.LOW || 0) /
                                  Math.max(1, total)) *
                                100
                              }%`
                            }}
                          />

                          <div
                            className="risk-bar medium"
                            style={{
                              width: `${
                                ((d.MEDIUM || 0) /
                                  Math.max(1, total)) *
                                100
                              }%`
                            }}
                          />

                          <div
                            className="risk-bar high"
                            style={{
                              width: `${
                                ((d.HIGH || 0) /
                                  Math.max(1, total)) *
                                100
                              }%`
                            }}
                          />

                        </>
                      );

                    })()}

                  </div>

                </div>

              </section>

            )}


            {/* High risk */}

            <HighRiskPanel
              highRisk={highRisk}
              formatAmount={formatAmount}
            />

          </>

        )}


        {/* ====================================================
            INVESTIGATIONS
        ==================================================== */}

        {activeSection === "investigations" && (

          <section className="panel investigation-panel">

            <div className="panel-header">

              <div>

                <p className="panel-label">
                  GRAPH INVESTIGATION
                </p>

                <h3>
                  Investigate customer connections
                </h3>

                <p className="panel-description">
                  Trace shared devices and identify
                  connected customers with fraud activity.
                </p>

              </div>

              <div className="graph-icon">
                ◎
              </div>

            </div>


            <form
              className="investigation-form"
              onSubmit={investigateCustomer}
            >

              <input
                type="text"
                placeholder="Enter customer ID e.g. CUS_27d8d40b"
                value={customerId}
                onChange={(e) =>
                  setCustomerId(e.target.value)
                }
              />

              <button
                type="submit"
                disabled={investigating}
              >
                {investigating
                  ? "Investigating..."
                  : "Investigate →"}
              </button>

            </form>


            {investigation &&
              !investigation.message && (

                <InvestigationResult
                  investigation={investigation}
                />

              )}


            {investigation?.message && (

              <div className="empty-state">

                <div>
                  ⌕
                </div>

                <strong>
                  {investigation.message}
                </strong>

              </div>

            )}

          </section>

        )}


        {/* ====================================================
            IDENTITY GRAPH
        ==================================================== */}

        {activeSection === "identity" && (

          <section className="panel investigation-panel">

            <div className="panel-header">

              <div>

                <p className="panel-label">
                  NEO4J IDENTITY GRAPH
                </p>

                <h3>
                  Customer identity connections
                </h3>

                <p className="panel-description">
                  Explore relationships between customers,
                  devices, IP addresses and merchants.
                </p>

              </div>

              <div className="graph-icon">
                ◇
              </div>

            </div>


            <form
              className="investigation-form"
              onSubmit={investigateCustomer}
            >

              <input
                type="text"
                placeholder="Enter customer ID e.g. CUS_27d8d40b"
                value={customerId}
                onChange={(e) =>
                  setCustomerId(e.target.value)
                }
              />

              <button
                type="submit"
                disabled={investigating}
              >
                {investigating
                  ? "Loading graph..."
                  : "Explore Graph →"}
              </button>

            </form>


            {investigation &&
              !investigation.message && (

                <div className="identity-summary">

                  <div className="identity-card">

                    <span>
                      CUSTOMER
                    </span>

                    <strong>
                      {investigation.customer_id}
                    </strong>

                  </div>


                  <div className="identity-card">

                    <span>
                      CONNECTED CUSTOMERS
                    </span>

                    <strong>
                      {investigation.connections?.length || 0}
                    </strong>

                  </div>


                  <div className="identity-card">

                    <span>
                      SHARED DEVICES
                    </span>

                    <strong>

                      {[
                        ...(investigation.connections || [])
                      ]
                        .reduce(
                          (total, connection) =>
                            total +
                            (connection.shared_devices?.length || 0),
                          0
                        )}

                    </strong>

                  </div>

                </div>

              )}


            {investigation &&
              !investigation.message && (

                <div className="connection-list">

                  {investigation.connections?.map(
                    (connection, index) => (

                      <div
                        className="connection-card"
                        key={index}
                      >

                        <div className="connection-main">

                          <div className="customer-avatar">
                            {connection.connected_customer
                              ?.slice(-2)
                              .toUpperCase()}
                          </div>

                          <div>

                            <span>
                              Connected customer
                            </span>

                            <strong>
                              {connection.connected_customer}
                            </strong>

                          </div>

                        </div>


                        <div className="connection-info">

                          <div>

                            <span>
                              Shared devices
                            </span>

                            <strong>
                              {
                                connection.shared_devices
                                  ?.length || 0
                              }
                            </strong>

                          </div>


                          <div>

                            <span>
                              Fraud transactions
                            </span>

                            <strong
                              className={
                                connection.fraud_transactions > 0
                                  ? "fraud-number"
                                  : ""
                              }
                            >
                              {
                                connection.fraud_transactions
                              }
                            </strong>

                          </div>

                        </div>


                        <div className="device-list">

                          {connection.shared_devices?.map(
                            (device) => (

                              <span key={device}>
                                {device}
                              </span>

                            )
                          )}

                        </div>

                      </div>

                    )
                  )}

                </div>

              )}

          </section>

        )}


        {/* ====================================================
            FOOTER
        ==================================================== */}

        <footer>

          <span>
            Credixis Risk Intelligence Platform
          </span>

          <span>
            Python • Spark • Kafka • PostgreSQL • Neo4j • FastAPI
          </span>

        </footer>

      </main>

    </div>
  );
}


// ============================================================
// Recent transactions component
// ============================================================

function RecentTransactions({
  riskResults,
  formatAmount,
  riskClass
}) {

  return (

    <section className="panel transactions-panel">

      <div className="panel-header">

        <div>

          <p className="panel-label">
            TRANSACTION MONITOR
          </p>

          <h3>
            Recent risk results
          </h3>

        </div>

        <span className="result-count">
          {riskResults.length} results
        </span>

      </div>


      <div className="table-wrapper">

        <table>

          <thead>

            <tr>

              <th>
                Transaction
              </th>

              <th>
                Customer
              </th>

              <th>
                Amount
              </th>

              <th>
                Risk score
              </th>

              <th>
                Risk level
              </th>

              <th>
                Fraud
              </th>

            </tr>

          </thead>


          <tbody>

            {riskResults.slice(0, 12).map(
              (transaction) => (

                <tr key={transaction.risk_id}>

                  <td className="transaction-id">
                    #{transaction.transaction_id}
                  </td>

                  <td>
                    {transaction.customer_id}
                  </td>

                  <td>
                    ₹
                    {formatAmount(transaction.amount)}
                  </td>

                  <td>

                    <div className="score-cell">

                      <div className="score-line">

                        <span
                          style={{
                            width: `${Math.min(
                              transaction.risk_score,
                              100
                            )}%`
                          }}
                        />

                      </div>

                      {transaction.risk_score}

                    </div>

                  </td>

                  <td>

                    <span
                      className={`risk-badge ${riskClass(
                        transaction.risk_level
                      )}`}
                    >
                      {transaction.risk_level}
                    </span>

                  </td>

                  <td>

                    {transaction.is_fraud ? (

                      <span className="fraud-badge">
                        DETECTED
                      </span>

                    ) : (

                      <span className="normal-badge">
                        NORMAL
                      </span>

                    )}

                  </td>

                </tr>

              )
            )}

          </tbody>

        </table>

      </div>

    </section>

  );
}


// ============================================================
// Investigation result component
// ============================================================

function InvestigationResult({
  investigation
}) {

  return (

    <div className="investigation-result">

      <div className="investigation-summary">

        <div>

          <span>
            Customer
          </span>

          <strong>
            {investigation.customer_id}
          </strong>

        </div>


        <div>

          <span>
            Connections found
          </span>

          <strong>
            {investigation.connections?.length || 0}
          </strong>

        </div>

      </div>


      <div className="connection-list">

        {investigation.connections?.map(
          (connection, index) => (

            <div
              className="connection-card"
              key={index}
            >

              <div className="connection-main">

                <div className="customer-avatar">

                  {connection.connected_customer
                    ?.slice(-2)
                    .toUpperCase()}

                </div>

                <div>

                  <span>
                    Connected customer
                  </span>

                  <strong>
                    {connection.connected_customer}
                  </strong>

                </div>

              </div>


              <div className="connection-info">

                <div>

                  <span>
                    Shared devices
                  </span>

                  <strong>
                    {connection.shared_devices?.length || 0}
                  </strong>

                </div>


                <div>

                  <span>
                    Fraud transactions
                  </span>

                  <strong
                    className={
                      connection.fraud_transactions > 0
                        ? "fraud-number"
                        : ""
                    }
                  >
                    {connection.fraud_transactions}
                  </strong>

                </div>

              </div>


              <div className="device-list">

                {connection.shared_devices?.map(
                  (device) => (

                    <span key={device}>
                      {device}
                    </span>

                  )
                )}

              </div>

            </div>

          )
        )}

      </div>

    </div>

  );
}


// ============================================================
// High risk component
// ============================================================

function HighRiskPanel({
  highRisk,
  formatAmount
}) {

  return (

    <section className="panel high-risk-panel">

      <div className="panel-header">

        <div>

          <p className="panel-label">
            ALERT CENTER
          </p>

          <h3>
            High-risk transactions
          </h3>

        </div>

        <span className="alert-count">
          {highRisk.length} alerts
        </span>

      </div>


      {highRisk.length === 0 ? (

        <div className="no-alerts">

          <div className="safe-icon">
            ✓
          </div>

          <div>

            <strong>
              No high-risk transactions
            </strong>

            <span>
              No HIGH risk results are currently
              present in the processed Kafka stream.
            </span>

          </div>

        </div>

      ) : (

        <div className="alert-list">

          {highRisk.slice(0, 20).map(
            (transaction) => (

              <div
                className="alert-row"
                key={transaction.risk_id}
              >

                <div>

                  <strong>
                    Transaction #{transaction.transaction_id}
                  </strong>

                  <span>
                    {transaction.customer_id}
                  </span>

                </div>


                <div>

                  <span>
                    Amount
                  </span>

                  <strong>
                    ₹
                    {formatAmount(transaction.amount)}
                  </strong>

                </div>


                <div>

                  <span>
                    Risk score
                  </span>

                  <strong className="fraud-number">
                    {transaction.risk_score}
                  </strong>

                </div>


                <span className="risk-badge risk-high">
                  HIGH
                </span>

              </div>

            )
          )}

        </div>

      )}

    </section>

  );
}


export default App;