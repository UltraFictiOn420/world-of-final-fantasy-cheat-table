-- UI-only guards for information rows. No writes to game memory or settings.
local list=getAddressList()
local owner=list.getMemoryRecordByID(1)
if not owner then return end
if WFF_InfoGuard and WFF_InfoGuard.owner~=owner then
  WFF_InfoGuard.cleanup()
end
if WFF_InfoGuard then return end
local state={owner=owner,records={},events={}}
WFF_InfoGuard=state
for _,id in ipairs({83,84,85}) do
  local r=list.getMemoryRecordByID(id)
  if r then
    r.Active=false
    r.Color=0x808080
    state.records[id]=true
    r.OnActivate=function(record,before,currentstate)
      if before then return false end
      return true
    end
  end
end
-- CE returns fresh Lua wrappers for records, so key by stable ID and ancestry,
-- not by userdata table keys. Block dialogs only for this feature's info rows.
-- Retain
-- any previous handlers and delegate every unrelated row to them unchanged.
for _,event in ipairs({'OnValueChange','OnAddressChange','OnTypeChange','OnDescriptionChange'}) do
  local previous=list[event]
  local handler=function(addresslist,record)
    if record and state.records[record.ID] then
      local parent=record.Parent
      if parent and parent.ID==80 then
        local ancestor=parent.Parent
        while ancestor do
          if ancestor.ID==1 then return true end
          ancestor=ancestor.Parent
        end
      end
    end
    if previous then return previous(addresslist,record) end
    return false
  end
  state.events[event]={previous=previous,handler=handler}
  list[event]=handler
end
state.cleanup=function()
  for event,binding in pairs(state.events) do
    if list[event]==binding.handler then list[event]=binding.previous end
  end
  if WFF_InfoGuard==state then WFF_InfoGuard=nil end
end
local previousDestroy=owner.OnDestroy
owner.OnDestroy=function()
  state.cleanup()
  if previousDestroy then previousDestroy() end
end
