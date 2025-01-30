pragma solidity ^0.8.0;

contract InvestorRegistry {
    struct Investment {
        address investor;
        string projectId;
        uint amount;
        uint timestamp;
    }

    mapping(string => Investment[]) public projectInvestments;
    mapping(address => bool) public registeredInvestors;
    address public admin;
    uint public minESGForFunding = 90;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Unauthorized");
        _;
    }

    function registerInvestor(address _investor) public onlyAdmin {
        registeredInvestors[_investor] = true;
    }

    function investInProject(string memory _projectId, uint _esgScore) public payable {
        require(registeredInvestors[msg.sender], "Not registered investor");
        require(_esgScore >= minESGForFunding, "Project ESG score too low");
        projectInvestments[_projectId].push(Investment(
            msg.sender,
            _projectId,
            msg.value,
            block.timestamp
        ));
    }

    function getInvestments(string memory _projectId) public view returns (Investment[] memory) {
        return projectInvestments[_projectId];
    }
}